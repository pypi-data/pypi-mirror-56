import numpy as np
import math
import matplotlib.pyplot as plt


def rotate(theta, alpha):
    A = np.array([[math.cos(theta), -math.sin(theta)],
                  [math.sin(theta), math.cos(theta)]])
    beta = A.dot(alpha)
    return beta, A


theta = 30/180*math.pi
alpha = np.array([math.sqrt(2)/2, math.sqrt(2)/2])
beta, A  = rotate(theta, alpha)


plt.axis('scaled')
plt.xlim([-1, 1])
plt.ylim([0, 1])
plt.xticks(np.arange(-1, 1, 0.5))
plt.yticks(np.arange(0, 1, 0.5))
plt.grid(linestyle='-.')

plt.quiver([0], [0], A[0,:], A[1,:], angles='xy', scale_units='xy',  scale=1)
plt.text(*A[:,0], '$a_1$', size=12)
plt.text(*A[:,1], '$a_2$', size=12)

plt.quiver([0], [0], alpha[0], alpha[1], angles='xy', scale_units='xy',  scale=1, color='b')
plt.quiver([0], [0], beta[0], beta[1], angles='xy', scale_units='xy',  scale=1, color='g')
plt.text(*alpha, '$\\alpha$', size=12)
plt.text(*beta, '$\\beta$', size=12)

plt.show()