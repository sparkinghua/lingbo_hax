import os
import numpy as np
import virtual_video_sender as v_sender

os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '-1'

RANDOM_SEED = 42
TRAIN_SET = './dataset/'


class Env():
    def __init__(self, random_seed=RANDOM_SEED, scale=1.):
        self.seed(random_seed)
        self.agent_id = random_seed
        self.sender = None
        self.traces = os.listdir(TRAIN_SET)
        self.scale = scale
        self._trace_idx = 0


    def seed(self, num=42):
        np.random.seed(num)

    def reset(self, actor_predict, actor_optimal=None):
        _delay = np.random.randint(1, 400)
        _queue = np.random.randint(1, 2000)
        _loss = np.random.randint(0, 30) / 100.
        _scale = np.random.randint(1,21)
        random = True
        _trace_idx = np.random.randint(len(self.traces))
        _trace = TRAIN_SET + self.traces[_trace_idx]
        std_flag = np.random.randint(0,4)
        self.sender = v_sender.VideoSender(_trace, _delay, _loss, _queue, _scale,random,std_flag)

        self.sender.set_actor(actor_predict)
        self.sender.set_actor_optimal(actor_optimal)
        self._trace_idx = _trace_idx

    def render(self):
        return

    def rollout(self, max_step=500):
        s_arr, a_arr, p_arr, r_arr,_,_,_ = self.sender.run(max_step)
        return s_arr, a_arr, p_arr, r_arr, self._trace_idx

if __name__ == "__main__":
    env_ = Env()
    env_.reset(None)
    env_.rollout()
