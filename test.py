import matplotlib.pyplot as plt

# 折线图
# x = [i for i in range(1, 11)]
# k1 = [1069.081, 1069.081, 1069.081, 1069.081, 1069.081, 1069.081, 1069.081, 1069.081, 1069.081, 1069.081]  # 100%
# plt.plot(x, k1, 's-', color='r', label="Dijkstra")  # s-:方形
# plt.xlabel("number of experiments", fontsize=16)  # 横坐标名字
# plt.ylabel("average time", fontsize=16)  # 纵坐标名字
# plt.legend(loc="best", fontsize=16)  # 图例
# plt.show()


# x = [i for i in range(1, 11)]
# k1 = [886.38, 867.057, 877.81, 880.957, 852.013, 858.631, 899.506, 869.731, 834.675, 852.192]  # 90%
# plt.plot(x, k1, 's-', color='r', label="90%")  # s-:方形
# plt.xlabel("number of experiments", fontsize=16)  # 横坐标名字
# plt.ylabel("average time", fontsize=16)  # 纵坐标名字
# plt.legend(loc="best", fontsize=16)  # 图例
# plt.show()


# x = [i for i in range(1, 11)]
# k1 = [701.639, 700.916, 705.938, 718.093, 722.722, 742.117, 726.131, 768.65, 722.579, 746.041]  # 80%
# plt.plot(x, k1, 's-', color='r', label="80%")  # s-:方形
# plt.xlabel("number of experiments", fontsize=16)  # 横坐标名字
# plt.ylabel("average time", fontsize=16)  # 纵坐标名字
# plt.legend(loc="best", fontsize=16)  # 图例
# plt.show()


# x = [i for i in range(1, 11)]
# k1 = [690.927, 685.186, 671.987, 688.682, 679.754, 682.527, 689.587, 689.264, 677.464, 690.783]  # 70%
# plt.plot(x, k1, 's-', color='r', label="70%")  # s-:方形
# plt.xlabel("number of experiments", fontsize=16)  # 横坐标名字
# plt.ylabel("average time", fontsize=16)  # 纵坐标名字
# plt.legend(loc="best", fontsize=16)  # 图例
# plt.show()


# x = [i for i in range(1, 11)]
# k1 = [708.489, 699.986, 695.856, 696.305, 700.358, 698.452, 688.072, 702.539, 706.499, 699.437]  # 60%
# plt.plot(x, k1, 's-', color='r', label="60%")  # s-:方形
# plt.xlabel("number of experiments", fontsize=16)  # 横坐标名字
# plt.ylabel("average time", fontsize=16)  # 纵坐标名字
# plt.legend(loc="best", fontsize=16)  # 图例
# plt.show()

x = [i for i in range(1, 11)]
k1 = [726.531, 720.826, 722.748, 723.074, 728.552, 712.958, 720.039, 728.765, 726.42, 724.658]  # 50%
plt.plot(x, k1, 's-', color='r', label="50%")  # s-:方形
plt.xlabel("number of experiments", fontsize=16)  # 横坐标名字
plt.ylabel("average time", fontsize=16)  # 纵坐标名字
plt.legend(loc="best", fontsize=16)  # 图例
plt.show()
