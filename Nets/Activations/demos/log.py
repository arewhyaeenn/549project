import matplotlib.pyplot as plt
import numpy as np
from math import exp, log


def LOG(x,b):
    if x > b:
        return log(b) + 2 - exp(-x/b + 1)
    elif x >= 1:
        return log(x) + 1
    else:
        return exp(x-1)


def LOG_prime(x,b):
    if x > b:
        return (log(b) + 2 - LOG(x,b)) / b
    elif x >= 1:
        return 1 / x
    else:
        return LOG(x,b)


b = 10
X = np.arange(-6,20,.01)
Y = np.array([LOG(x,b) for x in X])
Z = np.array([LOG_prime(x,b) for x in X])

fig = plt.figure(figsize=(15,6))
ax1 = plt.subplot(121)
ax1.plot(X,Y,label="$LOG(x,"+str(b)+")$")
ax2 = plt.subplot(122)
ax2.plot(X,Z,label="$LOG'(x,"+str(b)+")$")
ax1.plot([-6,20],[0,0],':k')
ax1.plot([0,0],[0,6],':k')
ax2.plot([-6,20],[0,0],':k')
ax2.plot([0,0],[0,1],':k')
ax1.set_title("$LOG(x,"+str(b)+")$")
ax2.set_title("$LOG\'(x,"+str(b)+")$")
plt.suptitle("Logarithmic Activation")