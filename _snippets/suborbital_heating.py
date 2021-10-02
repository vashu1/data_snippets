# https://space.stackexchange.com/questions/22804/if-there-was-a-non-rotating-skyhook-in-earth-orbit-what-would-re-entry-be-like/22829#22829

def deriv(X, t):

    x, v = X.reshape(2, -1)

    r, speed = [np.sqrt((thing**2).sum()) for thing in x, v]

    acc_g = -x * GMe *((x**2).sum())**-1.5

    alt = r - re

    rho    = rho0 * np.exp(-alt/hscale)
    Fdrag  = -0.5 * v * speed * CD * Area * rho
    n_lift = np.hstack((-v[1], v[0]))/speed   # definition of lift
    Flift  = LDR * 0.5 * n_lift * speed**2 * CD * Area * rho

    acc_d = (Fdrag + Flift)/m0

    return np.hstack((v, acc_g + acc_d))

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint as ODEint

pi  = np.pi
GMe = 3.986E+14

alt = 250000.   # meters
re  = 6378000.  # meters
v0  = 4260.     # m/s
hscales = [7000., 7500., 8000.]   # meters
CDs     = [0.2, 0.5, 0.8]
LDRs    = [0, 0.15, 0.3]
Area    = pi * 1.1**2             # m^2
m0      = 6800. # kg
rho0    = 1.25  # kg/m^3

X0   = np.array([0, re+alt, v0, 0])
dt   = 1.0      # seconds per reported value by the solver (internally variable timesteps)
time = np.arange(0, 301, dt)

answers = []

for CD in CDs:
    for hscale in hscales:
        for LDR in LDRs:

            answer, info = ODEint(deriv, X0, time, full_output = True)
            answers.append(answer)

km = 1E-03

gee = 9.8  # m/s^2

plt.figure()

for answer in answers:
    x, y, vx, vy = answer.T
    r = np.sqrt( x**2 +  y**2 )
    v = np.sqrt(vx**2 + vy**2)
    KE = 0.5 *m0 * v**2

    plt.subplot(5, 1, 1)
    plt.plot(time, km*vx)
    plt.plot(time, km*vy)
    plt.plot(time, km*v )
    plt.title('vx, vy, vtot (km/s) versus time (seconds)', fontsize=16)
    plt.subplot(5, 1, 2)
    plt.plot(time, km*(r-re))
    plt.title('altitude (km) versus time (seconds)', fontsize=16)
    plt.subplot(5, 1, 3)
    plt.plot(time[:-1], KE[:-1] - KE[1:])
    plt.title('Watts dissipated', fontsize=16)
    plt.subplot(5, 1, 4)
    plt.plot(time[:-1], ((v[:-1] - v[1:])/dt)/gee)
    plt.title('gees', fontsize=16)
    plt.subplot(5, 1, 5)
    plt.plot(km*x, km*(y-re))
    plt.plot(km*x, km*(np.sqrt(re**2 - x**2)-re), '-k', linewidth=2)
    plt.title('y versus x (km)', fontsize=16)
plt.show()