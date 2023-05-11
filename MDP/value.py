import time

from maze_generator import generate_maze
import matplotlib.pyplot as plt
from collections import deque
import numpy as np

# 定义迷宫地图及参数
aa = time.time()
size_list = [[21, 20], [41, 10], [81, 5]]
size = size_list[2][0]
width = size_list[2][1]
MAZE, ENTRANCE, EXIT = generate_maze(size, size)

maze = np.array(MAZE)
ex_y, ex_x = EXIT
goal = (ex_x, ex_y)
actions = ["up", "down", "left", "right"]
discount = 0.99
theta = 0.000000001

# 初始化价值函数
values = np.zeros(maze.shape)

# MDP值迭代算法
while True:
    delta = 0
    for i in range(1, maze.shape[0]):
        for j in range(maze.shape[1]):
            if maze[i, j] == 0:
                v = values[i, j]
                value_list = []
                for a in actions:
                    if a == "up":
                        next_state = (max(i - 1, 0), j)
                    elif a == "down":
                        next_state = (min(i + 1, maze.shape[0] - 1), j)
                    elif a == "left":
                        next_state = (i, max(j - 1, 0))
                    elif a == "right":
                        next_state = (i, min(j + 1, maze.shape[1] - 1))
                    if next_state == goal:
                        value_list.append(1)
                    else:
                        value_list.append(discount * values[next_state])
                values[i, j] = max(value_list)
                delta = max(delta, abs(v - values[i, j]))
    if delta < theta:
        break

en_y, en_x = ENTRANCE

dirs = [
    lambda x, y: (x, y + 1),  # 右
    lambda x, y: (x + 1, y),  # 下
    lambda x, y: (x, y - 1),  # 左
    lambda x, y: (x - 1, y),  # 上
]

fig, ax = plt.subplots(figsize=(10, 10))
# 初始化点
plt.imshow(MAZE, cmap='binary')
plt.title('MDP value iteration ')


# BFS
def solve_maze_with_queue(x1, y1, x2, y2):
    q = deque()
    path = []
    q.append((x1, y1, -1))
    ax.plot(y1, x1, 'ro', markersize=width, alpha=values[x1][y1])
    while len(q) > 0:
        cur_node = q.popleft()
        path.append(cur_node)
        if cur_node[:2] == (x2, y2):
            return True
        next_node = None
        next_value = 0
        for d in dirs:
            next_x, next_y = d(cur_node[0], cur_node[1])
            if values[next_x][next_y] >= next_value:
                next_node = (next_x, next_y)
                next_value = values[next_x][next_y]
        q.append((next_node[0], next_node[1], len(path) - 1))
        ax.plot(next_node[1], next_node[0], 'ro', markersize=width, alpha=values[next_node[0]][next_node[1]])
        # plt.pause(0.0001)
    return False



ex_y, ex_x = EXIT
solve_maze_with_queue(en_x, en_y, ex_x, ex_y)
print(time.time()-aa)
plt.show()
