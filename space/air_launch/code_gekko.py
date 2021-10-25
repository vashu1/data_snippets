# python3 -m pip install gekko

import numpy as np
import matplotlib.pyplot as plt
from gekko import GEKKO

# create GEKKO model
m = GEKKO()

# scale 0-1 time with tf
m.time = np.linspace(0,1,1001)

# options
m.options.NODES = 6
m.options.SOLVER = 3
m.options.IMODE = 6
m.options.MAX_ITER = 500
m.options.MV_TYPE = 0
m.options.DIAGLEVEL = 0

# final time
tf = m.FV(value=1.0,lb=0.1,ub=1000)
tf.STATUS = 1

# force
u = m.MV(value=0,lb=-1.1,ub=1.1)
u.STATUS = 1
u.DCOST = 1e-5

# variables
s = m.Var(value=0)
v = m.Var(value=0,lb=0,ub=1.7)
mass = m.Var(value=1,lb=0.2)

# differential equations scaled by tf
m.Equation(s.dt()==tf*v)
m.Equation(mass*v.dt()==tf*(u-0.2*v**2))
m.Equation(mass.dt()==tf*(-0.01*u**2))

# specify endpoint conditions
m.fix(s, pos=len(m.time)-1,val=1000_000)
m.fix(v, pos=len(m.time)-1,val=8000)

# minimize final time
m.Obj(tf)

# Optimize launch
m.solve()

print('Optimal Solution (final time): ' + str(tf.value[0]))

# scaled time
ts = m.time * tf.value[0]

# plot results
plt.figure(1)
plt.subplot(4,1,1)
plt.plot(ts,s.value,'r-',linewidth=2)
plt.ylabel('Position')
plt.legend(['s (Position)'])

plt.subplot(4,1,2)
plt.plot(ts,v.value,'b-',linewidth=2)
plt.ylabel('Velocity')
plt.legend(['v (Velocity)'])

plt.subplot(4,1,3)
plt.plot(ts,mass.value,'k-',linewidth=2)
plt.ylabel('Mass')
plt.legend(['m (Mass)'])

plt.subplot(4,1,4)
plt.plot(ts,u.value,'g-',linewidth=2)
plt.ylabel('Force')
plt.legend(['u (Force)'])

plt.xlabel('Time')
plt.show()