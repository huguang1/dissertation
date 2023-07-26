# from collections import Counter
#
# my_list = [1, 2, 3, 2, 1, 2, 3, 3, 3]
#
# counter = Counter(my_list)
# most_common = counter.most_common(1)
# most_common_value = most_common[0][0]
# print(most_common_value)
import random

s = 0
for _ in range(1000):
    if round(random.uniform(-0.1, 0.9)) == 0:
        s += 1
print(s)
