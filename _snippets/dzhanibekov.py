# model for - The Dzhanibekov effect, also called the intermediate axis theorem or tennis racket theorem
from math import cos, sin
import numpy as np
from matplotlib import animation
import matplotlib.pyplot as plt

oxyz = (0,0,0)
ox, oy, oz = (1, 0, 0), (0, 1, 0), (0, 0, 1)

I1 = 3
I2 = 2
I3 = 1
assert (I1 > I2 > I3) or (I1 < I2 < I3)  # we rotate around ox
s = 1e-3  # perturbation
w1 = s
w2 = 1
w3 = 0  # s or 0

dt = 1e-4

LEN = int(1e6)
print('turns', w2/6*LEN*dt)


def turn(ox, oy, a):
  xx, xy, xz = ox
  yx, yy, yz = oy
  xx_ = cos(a) * xx + sin(a) * yx
  xy_ = cos(a) * xy + sin(a) * yy
  xz_ = cos(a) * xz + sin(a) * yz
  yx_ = cos(a) * yx - sin(a) * xx
  yy_ = cos(a) * yy - sin(a) * xy
  yz_ = cos(a) * yz - sin(a) * xz
  return (xx_, xy_, xz_), (yx_, yy_, yz_)


def step():
  global I1, I2, I3, w1, w2, w3, dt, x, y, z, ox, oy, oz
  # https://ru.wikipedia.org/wiki/%D0%AD%D1%84%D1%84%D0%B5%D0%BA%D1%82_%D0%94%D0%B6%D0%B0%D0%BD%D0%B8%D0%B1%D0%B5%D0%BA%D0%BE%D0%B2%D0%B0
  # https://ru.wikipedia.org/wiki/%D0%A3%D1%80%D0%B0%D0%B2%D0%BD%D0%B5%D0%BD%D0%B8%D1%8F_%D0%AD%D0%B9%D0%BB%D0%B5%D1%80%D0%B0
  w_1 = (I2 - I3) * w2 * w3 / I1
  w_2 = (I3 - I1) * w3 * w1 / I2
  w_3 = (I1 - I2) * w1 * w2 / I3
  w1 += w_1 * dt
  w2 += w_2 * dt
  w3 += w_3 * dt
  # turn oxyz
  ox, oy = turn(ox, oy, w1 * dt)
  oy, oz = turn(oy, oz, w2 * dt)
  oz, ox = turn(oz, ox, w3 * dt)


def negative(v):
  x, y, z = v
  return (-x, -y, -z)


ws = []
axs = []
for _ in range(LEN):
  ws.append((w1, w2, w3))
  axs.append((ox, oy, oz))
  step()

l = len([i for i, (ws1, ws2) in enumerate(zip(ws, ws[1:])) if ws1[1]*ws2[1]<0])  # how many turns
print('tumbled', l)

fig = plt.figure()
#ax = fig.gca(projection='3d')  # deprecated, see next line
ax = fig.add_subplot(projection='3d')

L = int(LEN/l)*2
X, Y, Z = zip(*[ox for ox, oy, oz in axs[:L][::int(L/100)]])
plt.plot(X, Y, Z)

X, Y, Z = zip(*[oy for ox, oy, oz in axs[:L][::int(L/100)]])
plt.plot(X, Y, Z)

plt.show()

# plotlib animation

SECONDS = 10
N = 100
data = axs[:L][::int(L/100)]

fig = plt.figure()
ax = fig.add_subplot(projection='3d')


def gen(n):
    phi = 0
    while phi < 2*np.pi:
        yield np.array([np.cos(phi), np.sin(phi), phi])
        phi += 2*np.pi/n


def update(num, data, line):
    v = [data[num][0], oxyz, data[num][1], negative(data[num][1])]
    xs, ys, zs = zip(*v)
    line.set_data(xs, ys)
    line.set_3d_properties(zs)


line, = ax.plot(oxyz, oxyz)
ani = animation.FuncAnimation(fig, update, N, fargs=(data, line), interval=(SECONDS * 1_000)/N, blit=False)
#ani.save('dzhanibekov.gif', writer='imagemagick')
plt.show()

"""
  # https://ru.wikipedia.org/wiki/%D0%A3%D0%B3%D0%BB%D1%8B_%D0%AD%D0%B9%D0%BB%D0%B5%D1%80%D0%B0
  a, b, g = w1*dt, w2*dt, w3*dt
  xx = cos(a)*cos(g) - cos(b)*sin(a)*sin(g)
  xy = -cos(g)*sin(a) - cos(a)*cos(b)*sin(g)
  xz = sin(b)*sin(g)
  yx = cos(b)*cos(g)*sin(a) + cos(a)*sin(g)
  yy = cos(a)*cos(b)*cos(g) - sin(a)*sin(g)
  yz = -cos(g)*sin(b)
  zx = sin(a)*sin(b)
  zy = cos(a)*sin(b)
  zz = cos(b)
  x2 = xx * x + xy * y + xz * z
  y2 = yx * x + yy * y + yz * z
  z2 = zx * x + zy * y + zz * z
  x, y, z = x2, y2, z2
"""