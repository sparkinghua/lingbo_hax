import numpy as np
from collections import deque
import datagram_pb2
import copy

class socket(object):
    def __init__(self, trace_file = './fcc/raw_test/test_fcc_trace_216810_http---www.facebook.com_540', \
        basic_ms = 20., basic_loss = 0.1, basic_queue = 1000, \
        scale=1, random = True,min_rtt_std = 2,std_flag = 3):
        
        self.ms = basic_ms
        self.min_rtt = basic_ms *2
        self.min_rtt_std = min_rtt_std
        self.loss = basic_loss
        self.queue = basic_queue
        self.send_queue = deque()

        self.recv_queue = []
        self.recv_len = 0
        self.recv_base_ms = 0
        self.recv_idx = 0

        self.inflight_queue = deque()
        self.inflight_ttl = deque()
        self.min_rtt_queue = deque()
        self.trace_file = trace_file
        self.virtual_clock = 0
        self.base_ts = 0
        self.random = random
        self.tmp_ts = None
        self.scale = scale
        self.std_flag = std_flag
        self.rtt_ptr = 0
        self.times = []
        self.min_rtts = []
        self._load_trace()
        self._gen_rtt()
    def _gen_rtt(self):
        for time in range(1,150):
            self.times.append(100*time+np.random.uniform(-40., 40) )
            this_rtt = max(0, np.random.normal(self.min_rtt,self.min_rtt_std))
            self.min_rtts.append(this_rtt)
        self.times_o = self.times[:]
    
    def _load_trace(self):
        f = open(self.trace_file, 'r')
        arr = []
        for line in f:
            _line_ts = int(line)
            arr.append(_line_ts)
        f.close()

        # scale
        _scale = int(self.scale) - 1
        if _scale > 0:
            _tmp = []
            ptr = arr[0]
            for p in arr:
                scale_tmp = np.random.randint(ptr, p + 1, _scale)
                scale_tmp.sort()
                for _t in scale_tmp:
                    _tmp.append(int(_t))
                _tmp.append(p)
                ptr = p            
            self.recv_queue = _tmp
        else:
            self.recv_queue = arr
        self.recv_len = len(self.recv_queue)

        trace_duration = self.recv_queue[-1] - self.recv_queue[0]
        trace_count = self.recv_len


        if self.random:
            self.recv_idx = int(np.random.randint(self.recv_len))
        else:
            self.recv_idx = 0
        self.recv_base_ms = int(0 - self.recv_queue[self.recv_idx])

    def inflight_step(self, ts):
        for t in range(len(self.inflight_ttl)):
            self.inflight_ttl[t] -= 1.
        
        for t in range(len(self.inflight_ttl)):
            if self.inflight_ttl[0] <= 0.:
                # sendto
                if len(self.send_queue) < self.queue:

                    serialized_data, peer_addr = self.inflight_queue[0]
                    self.send_queue.append((serialized_data, peer_addr, ts))
                self.inflight_ttl.popleft()
                self.inflight_queue.popleft()
            else:
                break

    def sendto(self, serialized_data, peer_addr):
        _rand = np.random.uniform()
        if _rand > self.loss:
            self.inflight_queue.append((serialized_data, peer_addr))
            ack_str, ack = self.construct_ack_from_data(serialized_data)
  
            while self.times[self.rtt_ptr] < ack.send_ts:
                self.rtt_ptr += 1
                if self.rtt_ptr == len(self.times):
                    end_time = self.times[-1]
                    self.times = [time + end_time for time in self.times_o]
                    self.rtt_ptr = 0
            self.inflight_ttl.append(self.min_rtts[self.rtt_ptr] + np.random.uniform(0., 2) )

    def construct_ack_from_data(self, serialized_data):
        """Construct a serialized ACK that acks a serialized datagram."""

        data = datagram_pb2.Data()
        data.ParseFromString(serialized_data)

        ack = datagram_pb2.Ack()
        ack.seq_num = data.seq_num
        ack.send_ts = data.send_ts
        ack.sent_bytes = data.sent_bytes
        ack.delivered_time = data.delivered_time
        ack.delivered = data.delivered
        ack.ack_bytes = len(serialized_data)

        return ack.SerializeToString(), ack
    
    def get_optimal(self, curr_ts, future_ms = 100., est_ms = 800.):
        est_ms = self.std_flag * self.min_rtt_std + 10.
        # est_ms = 0
        _virtual_idx = self.recv_idx
        _virtual_base_ms = self.recv_base_ms
        _virtual_send_queue = copy.copy(self.send_queue)

        # start finding more
        _pkt_cnt = 0
        _duration = 0.
        
        for t in range(len(self.inflight_ttl)):
            serialized_data, _ = self.inflight_queue[t]
            ack_str, ack = self.construct_ack_from_data(serialized_data)
            _virtual_send_queue.append((None, None, self.inflight_ttl[t] + ack.send_ts))
        
        _queueing_delay_arr = []
        _virtual_future_ms = None
        _virtual_start = None
        while len(_virtual_send_queue) > 0:
            _, _, send_header = _virtual_send_queue[0]
            send_ttl = self.get_front()
            while send_ttl - send_header < 0:
                self.recv_inc()
                send_ttl = self.get_front()
            _virtual_send_queue.popleft()
            _virtual_start = float(send_ttl)
            _recv_duration = float(send_ttl) - curr_ts
            if _recv_duration > future_ms and _virtual_future_ms is None:
                _virtual_future_ms = _recv_duration
            _queueing_delay_arr.append(float(send_ttl) - float(send_header))

        if len(_queueing_delay_arr) > 0:
            _queueing_delay = np.mean(_queueing_delay_arr)
        else:
            _queueing_delay = 0.

        if _virtual_start is None:
            _virtual_start = self.get_front()



        while True:
            _pkt = self.get_front()
            if _pkt - curr_ts > future_ms and _virtual_future_ms is None:
                _virtual_future_ms = (_pkt - curr_ts)
            
            if _virtual_future_ms is None or _pkt - _virtual_start <= _virtual_future_ms:
                self.recv_inc()
                _pkt_cnt += 1
            else:
                _duration = _pkt - _virtual_start
                break

        # back to the future
        self.recv_idx = _virtual_idx
        self.recv_base_ms = _virtual_base_ms

        _pkt_cnt = max(_pkt_cnt, 0.)
        _tput = _pkt_cnt / _duration
        est_ms = min(self.queue/_tput, est_ms)
        _pkt_cnt += (_pkt_cnt / _duration * max(est_ms - _queueing_delay, 0.))
        _cwnd = _pkt_cnt / float(_duration) * (self.ms * 2.)
        return _cwnd

    def recv_inc(self):
        self.recv_idx += 1
        if self.recv_idx >= self.recv_len:
            self.recv_base_ms += self.recv_queue[self.recv_idx - 1]
            self.recv_idx = 0

    def get_front(self):
        _base = self.recv_queue[self.recv_idx] + self.recv_base_ms
        return _base

    def epoll(self, ts):
        can_send = False
        while True:
            _limbo_ms = self.get_front()
            if _limbo_ms <= ts and len(self.send_queue) > 0:
                _send_header = self.send_queue[0]
                serialized_data, peer_addr, send_ms = _send_header
                if send_ms <= _limbo_ms:
                    can_send = True
                    break
                else:
                    self.recv_inc()
            else:
                break
        return can_send

    def recvfrom(self, max_len):
        _send_header = self.send_queue[0]
        serialized_data, peer_addr, _ = _send_header
        self.send_queue.popleft()
        self.recv_inc()
        ack_str, ack = self.construct_ack_from_data(serialized_data)
        return ack_str, peer_addr

    def setblocking(self, block):
        pass

    def close(self):
        pass
        
