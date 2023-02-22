# Born time: 2022-5-10
# Latest update: 2022-5-11
# RL Training Phase
# Hengxi


import gym
import numpy as np
import torch
import torch.nn as nn
import random
import itertools
from agent import Agent

"""
gym is kind of reinforcement learning package.

"""



# BUFFER_SIZE = 500000
EPSILON_START = 1.0
EPSILON_END = 0.02
EPSILON_DECAY = 100000
TARGET_UPDATE_FREQUENCY = 10

env = gym.make("CartPole-v1")
s = env.reset()

n_state = len(s)
n_action = env.action_space.n

"""Generate agents"""

agent = Agent(idx=0,
              n_input=n_state,
              n_output=n_action,
              mode='train')

"""Main Training Loop"""

n_episode = 6000
n_time_step = 1000

REWARD_BUFFER = np.empty(shape=n_episode)
for episode_i in range(n_episode):
    # for episode_i in itertools.count():
    episode_reward = 0
    for step_i in range(n_time_step):
        epsilon = np.interp(episode_i * n_time_step + step_i, [0, EPSILON_DECAY],
                            [EPSILON_START, EPSILON_END])  # interpolation  这一部分是关于给小车一个随机抖动
        random_sample = random.random()
        if random_sample <= epsilon:
            a = env.action_space.sample()
        else:
            a = agent.online_net.act(s)    # 根据算法给模型设置抖动

        s_, r, done, info = env.step(a)  # info will not be used
        agent.memo.add_memo(s, a, r, done, s_)   # 将获得的经验进行记录
        s = s_
        episode_reward += r

        if done:
            # print(step_i,done)
            s = env.reset()
            REWARD_BUFFER[episode_i] = episode_reward
            break

        # After solved, watch it play
        if np.mean(REWARD_BUFFER[:episode_i]) >= 80:
            count = 0
            while True:
                a = agent.online_net.act(s)
                s, r, done, info = env.step(a)
                print(count,a)
                count += 1
                env.render()  # model for easily observing

                if done:
                    count = 0
                    env.reset()

        # Start Gradient Step  抽取部分记忆，为模型做出更好的记忆
        batch_s, batch_a, batch_r, batch_done, batch_s_ = agent.memo.sample()  # update batch-size amounts of Q

        # Compute Targets
        target_q_values = agent.target_net(batch_s_)   # 用最后一个观测来进行预测
        max_target_q_values = target_q_values.max(dim=1, keepdim=True)[0]  #
        targets = batch_r + agent.GAMMA * (1 - batch_done) * max_target_q_values  # 根据论文中的公式来计算。

        # Compute Q_values
        q_values = agent.online_net(batch_s)  # 实时的获取网络的状态
        a_q_values = torch.gather(input=q_values, dim=1, index=batch_a)  # 获取不同时候的状态的观测值

        # Compute Loss
        loss = nn.functional.smooth_l1_loss(a_q_values, targets)  # 将上面获取的几个值放到loss函数中

        # Gradient Descent
        agent.optimizer.zero_grad()   # 最后使用梯度下降方法来实现
        loss.backward()
        agent.optimizer.step()

    # Update target network
    # if episode_i % 1 == 0:
    if episode_i % TARGET_UPDATE_FREQUENCY == 0:  # 将每10轮的所有网络中的状态值全部进行替换
        agent.target_net.load_state_dict(agent.online_net.state_dict())

        # Print the training progress
        print("Episode: {}".format(episode_i))
        print("Avg. Reward: {}".format(np.mean(REWARD_BUFFER[:episode_i])))
