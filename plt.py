
from matplotlib import pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
ax = Axes3D(fig)
X = []
Y = []
for i in range(4):
    for j in range(4):
        X.append(i)
        Y.append(j)
print(X)
print(Y)

Z = [0, 243, 0, 0, 5, 0, 124, 231, 0, 0, 34, 21, 0, 3, 42, 34]

ax = plt.subplot(111, projection='3d')
ax.scatter(X, Y, Z, c='r')
ax.set_zlabel('pixel')  # 坐标轴
ax.set_ylabel('Y')
ax.set_xlabel('X')
plt.show()