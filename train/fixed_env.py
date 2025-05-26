import os
import numpy as np
import virtual_video_sender as v_sender

os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '-1'

RANDOM_SEED = 42
MAX_STEP = 500

class Env():
    def __init__(self, random_seed=RANDOM_SEED):
        self.seed(random_seed)
        self.agent_id = random_seed
        # variables below will be filled in during setup
        self.sender = None

    def seed(self, num=42):
        np.random.seed(num)

    def reset(self, actor_predict, trace_name, random, scale,_delay):
        # _delay = 250.
        _loss = 0.01 # np.random.randint(15) / 100.
        _queue = 500. # np.random.randint(20, 1000)
        self.sender = v_sender.VideoSender(trace_name, _delay, _loss, _queue, scale, random,3)
        self.sender.set_actor(actor_predict)

    def render(self):
        return

    def rollout(self):
        s_arr, a_arr, p_arr, r_arr, tputs,delays,losss = self.sender.run(MAX_STEP)

        entropy = np.mean(0.)
        reward = np.mean(r_arr)
        
        return entropy, reward,np.mean(tputs), np.mean(delays), np.mean(losss)
