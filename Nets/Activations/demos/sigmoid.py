import matplotlib.pyplot as plt
import numpy as np
from math import exp, log

def S(x):
    return 1 / (1 + exp(-x))


X = np.arange(-6,6,.01)
Y = np.array([S(x) for x in X])
Z = Y*(1-Y)

fig = plt.figure(figsize=(15,6))
ax1 = plt.subplot(121)
ax1.plot(X,Y,label="$S(x)$")
ax2 = plt.subplot(122)
ax2.plot(X,Z,label="$S'(x)$")
ax1.plot([-6,6],[0,0],':k')
ax1.plot([0,0],[0,1],':k')
ax2.plot([-6,6],[0,0],':k')
ax2.plot([0,0],[0,0.25],':k')
ax1.set_title('$S(x)$')
ax2.set_title('$S\'(x)$')
plt.suptitle("Sigmoid Activation")