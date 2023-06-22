from collections import Counter
import numpy as np
import random


class DQNLearn:
    store_count = 0
    store_size = 100  # buffer size
    decline = 0.6  # 衰减系数

    def __init__(self):
        self.learn_time = 0
        self.storage = np.zeros((self.store_size, 2))

    def get_action(self):
        if self.learn_time == 0 or random.randint(0, 100) < 100 * (self.decline ** self.learn_time):
            action = random.choice([1, 2])
        else:
            reward = self.storage[:, 1]
            r_order = np.argsort(reward)
            r_order = r_order[50:]
            action_list = self.storage[:, 0]
            new_list = [action_list[i] for i in r_order]
            new_list = [x for x in new_list if x != 0]
            counter = Counter(new_list)
            most_common = counter.most_common(1)
            most_common_value = most_common[0][0]
            action = most_common_value
        return action

    def store(self, action, reward):
        self.storage[self.store_count % self.store_size] = [action, reward]
        self.learn_time += 1


















