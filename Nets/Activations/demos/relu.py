import matplotlib.pyplot as plt
import numpy as np
from math import exp, log

def R(x):
    return max(0,x)


def R_prime(x):
    if x >= 0:
        return 1
    else:
        return 0


X = np.arange(-6,6,.01)
Y = np.array([R(x) for x in X])
Z = np.array([R_prime(x) for x in X])

fig = plt.figure(figsize=(15,6))
ax1 = plt.subplot(121)
ax1.plot(X,Y,label="$R(x)$")
ax2 = plt.subplot(122)
ax2.plot(X,Z,label="$R'(x)$")
ax1.plot([-6,6],[0,0],':k')
ax1.plot([0,0],[0,6],':k')
ax2.plot([-6,6],[0,0],':k')
ax2.plot([0,0],[0,1],':k')
ax1.set_title('$R(x)$')
ax2.set_title('$R\'(x)$')
plt.suptitle("ReLU")