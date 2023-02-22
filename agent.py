# Born time: 2022-5-10
# Latest update: 2022-5-11
# RL agent
# Hengxi

import numpy as np
import torch
import torch.nn as nn
import random


class ReplayMemory:
    def __init__(self, n_s, n_a):
        self.n_s = n_s
        self.n_a = n_a

        self.MEMORY_SIZE = 10000
        self.BATCH_SIZE = 64
        self.all_s = np.empty(shape=(self.MEMORY_SIZE, self.n_s), dtype=np.float64)
        self.all_a = np.random.randint(low=0, high=self.n_a, size=self.MEMORY_SIZE, dtype=np.uint8)
        self.all_r = np.empty(self.MEMORY_SIZE, dtype=np.float64)
        self.all_done = np.random.randint(low=0, high=2, size=self.MEMORY_SIZE, dtype=np.uint8)
        self.all_s_ = np.empty(shape=(self.MEMORY_SIZE, self.n_s), dtype=np.float64)
        self.count = 0
        self.t = 0

        # self.a1 = np.random.randint(low=0,high=)

    def add_memo(self, s, a, r, done, s_):  # 添加到记忆中
        self.all_s[self.t] = s
        self.all_a[self.t] = a
        self.all_r[self.t] = r
        self.all_done[self.t] = done
        self.all_s_[self.t] = s_
        self.count = max(self.count, self.t + 1)
        self.t = (self.t + 1) % self.MEMORY_SIZE

    def sample(self):  # 从记忆中提取需要的数据
        if self.count < self.BATCH_SIZE:
            indexes = range(0, self.count)
        else:
            indexes = random.sample(range(0, self.count), self.BATCH_SIZE)

        batch_s = []
        batch_a = []
        batch_r = []
        batch_done = []
        batch_s_ = []
        for idx in indexes:
            batch_s.append(self.all_s[idx])
            batch_a.append(self.all_a[idx])
            batch_r.append(self.all_r[idx])
            batch_done.append(self.all_done[idx])
            batch_s_.append(self.all_s_[idx])

        batch_s_tensor = torch.as_tensor(np.asarray(batch_s), dtype=torch.float32)
        batch_a_tensor = torch.as_tensor(np.asarray(batch_a), dtype=torch.int64).unsqueeze(-1)
        batch_r_tensor = torch.as_tensor(np.asarray(batch_r), dtype=torch.float32).unsqueeze(-1)
        batch_done_tensor = torch.as_tensor(np.asarray(batch_done), dtype=torch.float32).unsqueeze(-1)
        batch_s__tensor = torch.as_tensor(np.asarray(batch_s_), dtype=torch.float32)

        return batch_s_tensor, batch_a_tensor, batch_r_tensor, batch_done_tensor, batch_s__tensor


class DQN(nn.Module):  # 这个就是神经网络模块
    def __init__(self, n_input, n_output):
        super().__init__()  # Reuse the param of nn.Module
        in_features = n_input  # ?

        # nn.Sequential() # 这个就是神经网络
        self.net = nn.Sequential(
            nn.Linear(in_features, 64),
            nn.Tanh(),
            nn.Linear(64, n_output))

    def forward(self, x):  # 这个表示的就是前向神经网络
        return self.net(x)

    def act(self, obs):  # 这个需要的就是什么动作
        obs_tensor = torch.as_tensor(obs, dtype=torch.float32)
        q_values = self(obs_tensor.unsqueeze(0))  # ?
        max_q_index = torch.argmax(q_values)
        action = max_q_index.detach().item()  # get the idx of q
        return action


class Agent:
    def __init__(self, idx, n_input, n_output, mode="train"):
        self.idx = idx
        self.mode = mode
        self.n_input = n_input
        self.n_output = n_output

        self.GAMMA = 0.99   # 衰减率
        self.learning_rate = 1e-3  # 学习率

        self.memo = ReplayMemory(n_s=self.n_input, n_a=self.n_output)  # 将重要的状态进行计算

        # Initialize the replay buffer of agent i
        if self.mode == "train":
            self.online_net = DQN(self.n_input, self.n_output)
            self.target_net = DQN(self.n_input, self.n_output)

            self.target_net.load_state_dict(self.online_net.state_dict())  # copy the current state of online_net

            self.optimizer = torch.optim.Adam(self.online_net.parameters(), lr=self.learning_rate)
