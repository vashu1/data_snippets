from math import cos, sin

x, y, z = (0, 1, 0)

I1 = 3
I2 = 2
I3 = 1
assert I1 > I2 > I3
s = 1e-3
w1 = s
w2 = 1
w3 = 0  # s or 0

dt = 1e-3

LEN = int(1e6)
print('turns', w2/6/dt)

def step():
  global I1, I2, I3, w1, w2, w3, dt, x, y, z
  w_1 = (I2 - I3) * w2 * w3 / I1
  w_2 = (I3 - I1) * w3 * w1 / I2
  w_3 = (I1 - I2) * w1 * w2 / I3
  w1 += w_1 * dt
  w2 += w_2 * dt
  w3 += w_3 * dt
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


ws = []
ds = []
for _ in range(LEN):
  ws.append((w1, w2, w3))
  ds.append((x, y, z))
  step()


# [w[1] for w in ws][::100_000]
# [x[0] for x in ds][::100_000]

len([i for i, (ws1, ws2) in enumerate(zip(ws, ws[1:])) if ws1[1]*ws2[1]<0])  # how many turns

# len([w for w in ws if abs(w[0])>0.1])

from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
from matplotlib import cm

data = ds[:30_000][::200]
data = ds[:100_000][::1_000]
X, Y, Z = zip(*data)

fig = plt.figure()
ax = fig.gca(projection='3d')
plt.plot(X, Y, Z)

plt.show()