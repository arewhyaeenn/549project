import matplotlib.pyplot as plt
import numpy as np
from math import exp, log


def LR(x,l,b):
    if x > b:
        return b
    elif x >= 0:
        return x
    else:
        return 0


def LR_prime(x,l,b):
    if x > b:
        return l
    elif x >= 0:
        return 1
    else:
        return l


l = 0.05
b = 5
X = np.arange(-6,6,.01)
Y = np.array([LR(x,l,b) for x in X])
Z = np.array([LR_prime(x,l,b) for x in X])

fig = plt.figure(figsize=(15,6))
ax1 = plt.subplot(121)
ax1.plot(X,Y,label="$LR(x,"+str(l)+","+str(b)+")$")
ax2 = plt.subplot(122)
ax2.plot(X,Z,label="$LR'(x,"+str(l)+","+str(b)+")$")
ax1.plot([-6,6],[0,0],':k')
ax1.plot([0,0],[0,6],':k')
ax2.plot([-6,6],[0,0],':k')
ax2.plot([0,0],[0,1],':k')
ax1.set_title("$LR(x,"+str(l)+","+str(b)+")$")
ax2.set_title("$LR\'(x,"+str(l)+","+str(b)+")$")
plt.suptitle("Leaky ReLU")