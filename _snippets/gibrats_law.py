import random
from matplotlib import pyplot as plt
import matplotlib.animation as animation

N = 200
RATE = 1.1

state = [random.random() for _ in range(N)]
state.sort(reverse=True)

fig, ax = plt.subplots()
ax.set_yscale('log')
ax.set_xscale('log')
xdata = list(range(N))
ln, = plt.plot(xdata, state, 'ro')

def init2():
    #ax.set_xlim(0, 2*np.pi)
    #ax.set_ylim(-1, 1)
    return ln,

def init():
    ln.set_data([], [])
    return ln,

def update(frame):
    for indx in range(len(state)):
      state[indx] *= RATE
    ln.set_data(xdata, state)
    ax.set_ylim(min(state), max(state))
    return ln,

ani = animation.FuncAnimation(fig, update, frames=list(range(100)),
                    init_func=init)
plt.show()
