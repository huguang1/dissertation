from collections import Counter

my_list = [1, 2, 3, 2, 1, 2, 3, 3, 3]

counter = Counter(my_list)
most_common = counter.most_common(1)
most_common_value = most_common[0][0]
print(most_common_value)
