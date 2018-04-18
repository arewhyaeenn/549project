import matplotlib.pyplot as plt
import numpy as np
from math import exp, log


def EXP(x,b):
    if x > log(b):
        return 2 - exp(-x + log(b))
    else:
        return exp(x)/b


def EXP_prime(x,b):
    if x > log(b):
        return 2 - EXP(x,b)
    else:
        return EXP(x,b)


b = 10
X = np.arange(-6,10,.01)
Y = np.array([EXP(x,b) for x in X])
Z = np.array([EXP_prime(x,b) for x in X])

fig = plt.figure(figsize=(15,6))
ax1 = plt.subplot(121)
ax1.plot(X,Y,label="$EXP(x,"+str(b)+")$")
ax2 = plt.subplot(122)
ax2.plot(X,Z,label="$EXP'(x,"+str(b)+")$")
ax1.plot([-6,10],[0,0],':k')
ax1.plot([0,0],[0,2],':k')
ax2.plot([-6,10],[0,0],':k')
ax2.plot([0,0],[0,1],':k')
ax1.set_title("$EXP(x,"+str(b)+")$")
ax2.set_title("$EXP\'(x,"+str(b)+")$")
plt.suptitle("Exponential Activation")