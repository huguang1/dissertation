from maze_generator import generate_maze
import matplotlib.pyplot as plt
from collections import deque
import numpy as np


size_list = [[21, 20], [41, 10], [81, 5]]
size = size_list[0][0]
width = size_list[0][1]
MAZE, ENTRANCE, EXIT = generate_maze(size, size)
en_y, en_x = ENTRANCE
ex_y, ex_x = EXIT
rewards = np.array(MAZE)
rewards *= -10
rewards[ex_x][ex_y] = 1
rewards = np.array(rewards).astype("float32")
rewards = rewards.ravel()

gamma = 0.9
n_states = size ** 2
n_actions = 4
P = np.zeros((n_states, n_actions, n_states)).astype("float32")
for s in range(n_states):

    P[s, 0, s-size if s-size >= 0 else s] = 1.0  # Up
    P[s, 1, s+size if s+size < n_states else s] = 1.0  # Down
    P[s, 2, s-1 if s % size != 0 else s] = 1.0  # Left
    P[s, 3, s+1 if (s+1) % size != 0 else s] = 1.0  # Right

# Initialization
policy = np.zeros(n_states).astype("int")
V = np.zeros(n_states).astype("float32")
done = False

while not done:
    # Policy Evaluation
    while True:
        delta = 0
        for s in range(n_states):
            v = V[s]
            V[s] = np.sum(P[s, policy[s]] * (rewards + gamma * V))
            delta = max(delta, np.abs(v - V[s]))
        if delta < 1e-3:
            break

    # Policy Improvement
    policy_stable = True
    for s in range(n_states):
        old_action = policy[s]
        q_values = np.zeros(n_actions)
        for a in range(n_actions):
            q_values[a] = np.sum(P[s, a] * (rewards + gamma * V))
        policy[s] = np.argmax(q_values)
        if old_action != policy[s]:
            policy_stable = False
    if policy_stable:
        done = True

# Display the results
actions = ['U', 'D', 'L', 'R']
for s in range(n_states):
    if policy[s] == 0:
        print(actions[0], end=' ')
    elif policy[s] == 1:
        print(actions[1], end=' ')
    elif policy[s] == 2:
        print(actions[2], end=' ')
    elif policy[s] == 3:
        print(actions[3], end=' ')
    if (s+1) % size == 0:
        print("")

fig, ax = plt.subplots(figsize=(10, 10))
# 初始化点
plt.imshow(MAZE, cmap='binary')
plt.title('MDP policy iteration ')
policy = policy.reshape((size, size))


dirs = [
    lambda x, y: (x - 1, y),  # 上
    lambda x, y: (x + 1, y),  # 下
    lambda x, y: (x, y - 1),  # 左
    lambda x, y: (x, y + 1),  # 右
]


def solve_maze_with_queue(x1, y1, x2, y2):
    q = deque()
    path = []
    q.append((x1, y1, -1))
    ax.plot(y1, x1, 'ro', markersize=width)
    while len(q) > 0:
        cur_node = q.popleft()
        path.append(cur_node)
        if cur_node[:2] == (x2, y2):
            return True
        next_x, next_y = dirs[policy[cur_node[0]][cur_node[1]]](cur_node[0], cur_node[1])
        q.append((next_x, next_y, len(path) - 1))
        ax.plot(next_y, next_x, 'ro', markersize=width)
        # plt.pause(0.0001)
    return False


solve_maze_with_queue(en_x, en_y, ex_x, ex_y)


# print(policy)
plt.show()





