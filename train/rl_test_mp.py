import os
import sys
os.environ['CUDA_VISIBLE_DEVICES']='-1'
import numpy as np
import fixed_env as env
import tensorflow.compat.v1 as tf
import multiprocessing as mp
import network as network


S_INFO = 9
S_LEN = 8
A_DIM = 1
RANDOM_SEED = 42
ACTOR_LR_RATE = 1e-4
NN_MODEL = sys.argv[1]
PPO_TRAINING_EPO = 5
LOG_FILE = './test_results/log_sim_rl'
NUM_AGENTS = 9
    
def agent(_traces):
    np.random.seed(RANDOM_SEED)
    net_env = env.Env()
    with tf.Session() as sess:

        actor = network.Network(sess,
                                 state_dim=[S_INFO, S_LEN], action_dim=A_DIM,
                                 learning_rate=ACTOR_LR_RATE)

        sess.run(tf.global_variables_initializer())
        saver = tf.train.Saver()  # save neural net parameters

        # restore neural net parameters
        if NN_MODEL is not None:  # NN_MODEL is the path to file
            saver.restore(sess, NN_MODEL)


        def predict(obs):
            action_prob = actor.predict(obs)

            return action_prob


        for p in _traces:
            _trace = './fcc/test/' + p

            _delay = 250
            net_env.reset(predict, _trace, False, 1, _delay)
            entropy, reward,tput,delay,loss = net_env.rollout()

            log_file = open(LOG_FILE + '_' + str(p), 'w')
            log_file.write(str(entropy) + '\t' +
                            str(reward) + '\t' +
                            str(tput)+ '\t' +
                            str(delay)+ '\t' +
                             str(loss)+
                            '\n')
            log_file.flush()
            log_file.close()


def main():

    np.random.seed(RANDOM_SEED)

    _traces_list = []
    for i in range(NUM_AGENTS):
        _traces_list.append([])

    _idx = 0
    for t in os.listdir('./fcc/test/'):
        _traces_list[_idx].append(t)
        _idx += 1
        _idx %= NUM_AGENTS

    agents = []
    for i in range(NUM_AGENTS):
        agents.append(mp.Process(target=agent,
                                 args=(_traces_list[i], )))

    for i in range(NUM_AGENTS):
        agents[i].start()

    for i in range(NUM_AGENTS):
        agents[i].join()

    # exit(0)

if __name__ == '__main__':
    main()