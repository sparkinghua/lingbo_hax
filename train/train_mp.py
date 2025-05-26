import multiprocessing as mp
import numpy as np
import logging
import os
import sys
import env as video_env
import network as network
import pool
import tensorflow.compat.v1 as tf
from tqdm import tqdm

os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

S_DIM = [9, 8]
A_DIM = 1

ACTOR_LR_RATE = 1e-4

NUM_AGENTS = 64
TRAIN_SEQ_LEN = 100  # take as a train batch
TRAIN_EPOCH = 1000000
MODEL_SAVE_INTERVAL = 50
RANDOM_SEED = 42

SUMMARY_DIR = './model'
TEST_LOG_FOLDER = './test_results/'
LOG_FILE = SUMMARY_DIR + '/log'


# create result directory
if not os.path.exists(SUMMARY_DIR):
    os.makedirs(SUMMARY_DIR)

NN_MODEL = None    

def testing(epoch, nn_model, log_file):
    # clean up the test results folder
    os.system('rm -r ' + TEST_LOG_FOLDER)


    if not os.path.exists(TEST_LOG_FOLDER):
        os.makedirs(TEST_LOG_FOLDER)
    # run test script
    os.system('python rl_test_mp.py ' + nn_model)

    # append test performance to the log
    rewards, entropies = [], []
    test_log_files = os.listdir(TEST_LOG_FOLDER)
    for test_log_file in test_log_files:
        reward, entropy = [], []
        with open(TEST_LOG_FOLDER + test_log_file, 'rb') as f:
            for line in f:
                parse = line.split()
                try:
                    entropy.append(float(parse[0]))
                    reward.append(float(parse[1]))
                except IndexError:
                    break
        rewards.append(np.mean(reward))
        entropies.append(np.mean(entropy))

    rewards = np.array(rewards)

    rewards_min = np.min(rewards)
    rewards_5per = np.percentile(rewards, 5)
    rewards_mean = np.mean(rewards)
    rewards_median = np.percentile(rewards, 50)
    rewards_95per = np.percentile(rewards, 95)
    rewards_max = np.max(rewards)

    log_file.write(str(epoch) + '\t' +
                   str(rewards_min) + '\t' +
                   str(rewards_5per) + '\t' +
                   str(rewards_mean) + '\t' +
                   str(rewards_median) + '\t' +
                   str(rewards_95per) + '\t' +
                   str(rewards_max) + '\n')
    log_file.flush()

    return rewards_mean, np.mean(entropies)
        
def central_agent(net_params_queues, exp_queues):

    assert len(net_params_queues) == NUM_AGENTS
    assert len(exp_queues) == NUM_AGENTS

    config=tf.ConfigProto(allow_soft_placement=True,
                    intra_op_parallelism_threads=1,
                    inter_op_parallelism_threads=1)
    config.gpu_options.allow_growth = True
    with tf.device('/gpu:0'):
        with tf.Session(config = config) as sess, open(LOG_FILE + '_test.txt', 'w') as test_log_file:
            summary_ops, summary_vars = build_summaries()

            actor_pool = pool.pool()
            actor = network.Network(sess, 
                    state_dim=S_DIM, action_dim=A_DIM,
                    learning_rate=ACTOR_LR_RATE)

            sess.run(tf.global_variables_initializer())

            writer = tf.summary.FileWriter(SUMMARY_DIR, sess.graph)  # training monitor
            saver = tf.train.Saver(max_to_keep=1000)  # save neural net parameters

            # restore neural net parameters
            nn_model = NN_MODEL
            if nn_model is not None:  # nn_model is the path to file
                saver.restore(sess, nn_model)
                print("Model restored.")

            env_pool = pool.pool()

            # synchronize the network parameters of work agent
            actor_net_params = actor.get_network_params()
            for agent in range(NUM_AGENTS):
                net_params_queues[agent].put(actor_net_params)

            for epoch in tqdm(range(TRAIN_EPOCH)):
                for agent in range(NUM_AGENTS):
                    s_batch, a_batch, r_batch = exp_queues[agent].get()
                    for (s_, a_) in zip(s_batch, a_batch):
                        env_pool.submit(s_, a_)
                    s_batch, a_batch = env_pool.get()
                    actor.train(s_batch, a_batch)
                    

                # synchronize the network parameters of work agent
                actor_net_params = actor.get_network_params()
                for agent in range(NUM_AGENTS):
                    net_params_queues[agent].put(actor_net_params)
                    
                if epoch % MODEL_SAVE_INTERVAL == 0:
                    # Save the neural net parameters to disk.
                    save_path = saver.save(sess, SUMMARY_DIR + "/nn_model_ep_" +
                                        str(epoch) + ".ckpt")

                    avg_reward, avg_entropy = testing(epoch,
                        SUMMARY_DIR + "/nn_model_ep_" + str(epoch) + ".ckpt", 
                        test_log_file)

                    summary_str = sess.run(summary_ops, feed_dict={
                        summary_vars[0]: avg_reward
                    })

                    writer.add_summary(summary_str, epoch)
                    writer.flush()

def agent(agent_id, net_params_queue, exp_queue):
    env = video_env.Env(agent_id)
    with tf.device('/cpu:0'):
        with tf.Session() as sess:
            actor = network.Network(sess,
                                    state_dim=S_DIM, action_dim=A_DIM,
                                    learning_rate=ACTOR_LR_RATE)
                        
            def predict(obs):
                action_prob = actor.predict(obs)
                return action_prob

            # initial synchronization of the network parameters from the coordinator
            actor_net_params = net_params_queue.get()
            actor.set_network_params(actor_net_params)
            # env.reset()
            for epoch in range(TRAIN_EPOCH):
                env.reset(predict)
                s_batch, a_batch, p_batch, r_batch, _ = env.rollout(TRAIN_SEQ_LEN)
                print('has_done')
                exp_queue.put([s_batch, a_batch, r_batch])

                actor_net_params = net_params_queue.get()
                actor.set_network_params(actor_net_params)

def build_summaries():
    reward = tf.Variable(0.)
    tf.summary.scalar("Reward", reward)

    summary_vars = [reward]
    summary_ops = tf.summary.merge_all()

    return summary_ops, summary_vars

def main():

    np.random.seed(RANDOM_SEED)

    # inter-process communication queues
    net_params_queues = []
    exp_queues = []
    for i in range(NUM_AGENTS):
        net_params_queues.append(mp.Queue(10000))
        exp_queues.append(mp.Queue(10000))

    # create a coordinator and multiple agent processes
    # (note: threading is not desirable due to python GIL)
    coordinator = mp.Process(target=central_agent,
                             args=(net_params_queues, exp_queues))
    coordinator.start()

    agents = []
    for i in range(NUM_AGENTS):
        agents.append(mp.Process(target=agent,
                                 args=(i,
                                       net_params_queues[i],
                                       exp_queues[i])))
    for i in range(NUM_AGENTS):
        agents[i].start()

    # wait unit training is done
    coordinator.join()


if __name__ == '__main__':
    main()
