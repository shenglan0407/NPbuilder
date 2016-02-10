import sys
import pylab as plt
import numpy as np
from mpl_toolkits.mplot3d import axes3d,Axes3D

coors = np.loadtxt( sys.argv[1],delimiter=" ")

X = coors[:,0]
Y = coors[:,1]
Z = coors[:,2]

fig = plt.figure(1)
plt.figure(1)
ax = Axes3D(fig)

#X = coordinates[0:len(coordinates):3]
#Y = coordinates[1:len(coordinates):3]
#Z = coordinates[2:len(coordinates):3]

surf = ax.scatter(X, Y, Z,s=100,c='r')
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")

plt.show()


