import time
import virtual_sock as sock
import numpy as np
import datagram_pb2

S_INFO = 9
S_LEN = 8
ACTIONS = [-1., 1.]
A_DIM = len(ACTIONS)
MAX_STEP = 1000
MAX_TIME_OUT = 30
MAX_LOSS = 100

class VideoSender(object):

    def curr_ts_ms(self):
        return int(self.virtual_clock)

    def __init__(self, trace, delay, loss, queue, scale=1, random=True,std_flag=3):
        if not random:
            np.random.seed(42)
        else:
            np.random.seed()

        self.init_ts = None
        self.virtual_clock = 0
        self.peer_addr = ('127.0.0.1', 42)
        self.scale = scale
        self.random = random
       

        self.dummy_payload = 'x' * 1400
        self.predict = None
        self.optimal = None

        # congestion control related
        self.seq_num = 0
        self.next_ack = 0
        self.cwnd = 2.0
        self.step_len_ms = 100

        # state variables for RLCC
        self.delivered_time = 0
        self.delivered = 0
        self.sent_bytes = 0
        
        self.min_rtt = 2 * delay 
        self.min_min_rtt = float('inf')
        self.trace = trace
        self.min_rtt_std =  self.min_rtt * np.random.uniform(0,0.3)
        if np.random.uniform(0,1) < 0.1:
            self.min_rtt_std = np.random.uniform(0,3)
        if not random:
            self.min_rtt_std = 50

        self.std_flag = std_flag
        self.sock = sock.socket(trace, delay, loss, queue, self.scale, random,self.min_rtt_std,self.std_flag)

        self.curr_rtt = 0.
        self.max_bw = 0.

        self.delay_ewma = None
        self.send_rate_ewma = None
        self.delivery_rate_ewma = None

        self.step_start_ms = None
        self.running = True
        self.state = np.zeros([S_INFO, S_LEN])

        self.step_cnt = 0
        self.done = False
        self.start_time = None

        self.ts_first = None
        self.rtt_buf = []
        self.thr_buff = []
        self.loss_buff = []

        self.loss = 0.

        self.s_batch, self.a_batch, self.p_batch, self.r_batch = [], [], [], []
        self.curr_bytes, self.curr_delay = [], []
        self.tput_batch, self.delay_batch, self.loss_batch = [], [], []

    def cleanup(self):
        self.sock.close()

    def handshake(self):
        self.sock.setblocking(0)  # non-blocking UDP socket

    def loss_ratio(self):
        self.loss_buff.sort()

        cnt = 0
        while True:
            now_ =  self.loss_buff[-1][0]
            send_ts_, seq_num_ = self.loss_buff[cnt]
            if now_ - send_ts_ > MAX_LOSS:
                cnt += 1
            else:
                break
        self.loss_buff = self.loss_buff[cnt:]
        
        tmp_loss = []
        for t in self.loss_buff:
            send_ts_, seq_num_ = t
            tmp_loss.append(seq_num_)

        if len(tmp_loss) > 0:
            loss_count = len(tmp_loss)
            loss_sum = tmp_loss[-1] - tmp_loss[0] + 1
            loss_ = 1. - loss_count / float(loss_sum)
        else:
            loss_ = 0.


        return loss_

    def update_state(self, ack):
        self.loss_buff.append([ack.send_ts, ack.seq_num])

        self.next_ack = max(self.next_ack, ack.seq_num + 1)
        curr_time_ms = self.curr_ts_ms()

        # Update RTT
        rtt = float(curr_time_ms - ack.send_ts)
        self.min_min_rtt = min(self.min_min_rtt, rtt)

        self.curr_rtt = rtt

        if self.ts_first is None:
            self.ts_first = curr_time_ms
        self.rtt_buf.append(rtt)
        

        delay = rtt - self.min_rtt 
        
        if self.delay_ewma is None:
            self.delay_ewma = delay
        else:
            self.delay_ewma = 0.875 * self.delay_ewma + 0.125 * delay

        # Update BBR's delivery rate
        self.delivered += ack.ack_bytes
        self.delivered_time = curr_time_ms
        delivery_rate = (0.008 * (self.delivered - ack.delivered) /
                         max(1, self.delivered_time - ack.delivered_time))
        
        if self.delivery_rate_ewma is None:
            self.delivery_rate_ewma = delivery_rate
        else:
            self.delivery_rate_ewma = (
                0.875 * self.delivery_rate_ewma + 0.125 * delivery_rate)

        self.max_bw = max(self.max_bw, self.delivery_rate_ewma)
        # update cum states
        self.curr_bytes.append(ack.ack_bytes)
        # print(delay, rtt, self.min_min_rtt)
        self.curr_delay.append(delay)

        # Update Vegas sending rate
        send_rate = 0.008 * (self.sent_bytes - ack.sent_bytes) / max(1, rtt)

        if self.send_rate_ewma is None:
            self.send_rate_ewma = send_rate
        else:
            self.send_rate_ewma = (
                0.875 * self.send_rate_ewma + 0.125 * send_rate)

    def take_action(self, action_idx):
        action_idx = np.clip(action_idx, -1., 1.)

        self.cwnd *= (1. + action_idx)
        self.cwnd = max(self.cwnd, 2.)
        self.cwnd = min(self.cwnd, 5000.)

    def send(self):

        data = datagram_pb2.Data()
        data.seq_num = self.seq_num
        data.send_ts = self.curr_ts_ms()
        data.sent_bytes = self.sent_bytes
        data.delivered_time = self.delivered_time
        data.delivered = self.delivered
        data.payload = self.dummy_payload

        serialized_data = data.SerializeToString()
        self.sock.sendto(serialized_data, self.peer_addr)
        self.seq_num += 1
        self.sent_bytes += len(serialized_data)
        

    def step(self, current_state, duration):
        state = np.roll(self.state, -1, axis=1)
        for p in range(S_INFO):
            state[p, -1] = current_state[p]

        if self.predict:
            action_prob = self.predict(state)
            act = action_prob[0]
        else:
            action_prob = []
            act = 0. #np.random.randint(A_DIM)

        self.virtual_clock += np.random.uniform(0.9, 1.1) * 0.4



        # compute optimal: cwnd
        cwnd_optimal = self.sock.get_optimal(self.curr_ts_ms(), self.step_len_ms)
        cwnd_optimal = max(cwnd_optimal, 1.)

        _label = np.clip((cwnd_optimal - self.cwnd) / (self.cwnd + 1e-6), ACTIONS[0], ACTIONS[1])
        
        if self.optimal:
            self.optimal(state, [_label])

        self.s_batch.append(np.copy(self.state))
        self.a_batch.append([_label])
        self.p_batch.append([act])

        # compute reward
        cum_bytes = np.sum(self.curr_bytes)
        # bytes / 1000 / ms -> kb / ms -> mb / s
        _throughput = 0.008 * cum_bytes / (duration + 1e-6) # mbps
        _delay = np.mean(self.curr_delay) # s
        _reward = _throughput - 2. * _delay / 1000.
        self.tput_batch.append(_throughput)
        self.delay_batch.append(_delay/1000.0)
        self.loss_batch.append(self.loss)
        self.r_batch.append([_reward])
        
        # clean curr_buff
        self.curr_bytes = []
        self.curr_delay = []

        self.state = state

        return self.state, act, action_prob, _label

    def recv(self, max_steps = 300):
        serialized_ack, addr = self.sock.recvfrom(1600)

        if serialized_ack is None:
            return -1
        if addr != self.peer_addr:
            return -2
            
        ack = datagram_pb2.Ack()

        ack.ParseFromString(serialized_ack)

        self.update_state(ack)

        if self.step_start_ms is None:
            self.step_start_ms = self.curr_ts_ms()

        # At each step end, feed the state:
        duration_ = self.curr_ts_ms() - self.step_start_ms
        if duration_ > self.step_len_ms:  # step's end
            self.loss = self.loss_ratio()

            s = [self.delay_ewma / 100.,
                     self.delivery_rate_ewma / 20.,
                     self.send_rate_ewma / 20.,
                    self.loss,
                    self.cwnd / 500.,
                      duration_ / 100.,
                     self.min_rtt/100.,
                     self.min_rtt_std/10.,
                     self.std_flag/10.]
            
            state, action, prob, label = self.step(s, duration_)

            self.take_action(action)

            self.delay_ewma = None
            self.delivery_rate_ewma = None
            self.send_rate_ewma = None

            self.step_start_ms = self.curr_ts_ms()

            self.step_cnt += 1
            
            if self.step_cnt == max_steps:
                self.step_cnt = 0
                self.running = False
                self.done = True
        return 0

    def set_actor(self, actor_predict):
        self.predict = actor_predict

    def set_actor_optimal(self, actor_optimal):
        self.optimal = actor_optimal

    def run(self, max_step = MAX_STEP):
        VIDEO_CHUNK_COUNT = 1
        MAX_SEND_CHUNK_SIZE = 1.
        cum_delivered = 0
        cum_sent = 0
        for p in range(VIDEO_CHUNK_COUNT):
            # state variables for RLCC
            self.delivered_time = 0
            self.delivered = 0
            self.sent_bytes = 0
            self.running = True
            self.step_cnt = 0
            self.done = False
            

            send_chunk_size = np.random.uniform(0.9, 1.1) * MAX_SEND_CHUNK_SIZE
            
            self.single_step(max_step)
            
            cum_delivered += self.delivered
            cum_sent += self.sent_bytes


            
        self.r_batch.append([0.])
    
        return self.s_batch, self.a_batch, self.p_batch, self.r_batch[1:],np.mean(self.tput_batch), np.mean(self.delay_batch), np.mean(self.loss_batch)
            

    def window_is_open(self):
        return self.seq_num - self.next_ack < self.cwnd

    def single_step(self, max_steps=500, time_out=30.):
        step_time_out = 1000.
        last_clock = self.curr_ts_ms()
        while self.running:
            _curr_time = self.curr_ts_ms()
            if _curr_time - last_clock >= step_time_out:
                self.send()
                last_clock = self.curr_ts_ms()

            while self.sock.epoll(self.curr_ts_ms()):
                self.recv(max_steps)
                last_clock = self.curr_ts_ms()
            
            while self.window_is_open():
                self.send()
                last_clock = self.curr_ts_ms()

            self.virtual_clock += 1.
            
            self.sock.inflight_step(self.virtual_clock)


 
        
