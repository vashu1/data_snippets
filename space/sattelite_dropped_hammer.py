import math
from cdecimal import Decimal
import numpy as np

dt = np.float64(0.01) # seconds

G = np.float64(6.673848e-11)
M = np.float64(5.97219e24)

# satellite
m = np.float64(1000.0) # kg
s = np.float64(1.0) # m2

# Earth
R = np.float64(6.371e6) # meters
H = np.float64(300 * 1000.0) # meters

def h(x, y):
    return np.float64(math.sqrt(x * x + y * y))
    
def g(x, y):
    h0 = h(x, y)
    return G * M / (h0 * h0)

# test `dens()`
#print dens(0, R +   0)
#print (dens(0, R +  50 *1000.0) - 1.03e-3) / 1.03e-3
#print (dens(0, R +  80 *1000.0) - 1.85e-5) / 1.85e-5
#print (dens(0, R + 100 *1000.0) - 5.55e-7) / 5.55e-7
#print (dens(0, R + 150 *1000.0) - 2.0e-9) / 2.0e-9
#print (dens(0, R + 200 *1000.0) - 2.52e-10) / 2.52e-10

V =  np.float64(math.sqrt(G * M / (R + H)))-1 # m/s

nx = np.float64(0.0)
ny = R + H

x = nx + dt * V
y = ny - g(nx, ny) * dt * dt / np.float64(2)+ dt * 0

t = np.float64(0.0) # seconds
i = 0    
prevH = H
prevV = V

# calculation cycle
while True:
    x1 = x / h(x, y)
    y1 = y / h(x, y)
    agravitation = g(x, y)
    axg = - x1 * agravitation
    ayg = - y1 * agravitation
    dx = 2 * (x - nx) + axg * dt * dt
    dy = 2 * (y - ny) + ayg * dt * dt
    v = h(dx, dy) / (2 * dt)

    ax = axg
    ay = ayg
    px = 2 * x - nx + ax * dt * dt
    py = 2 * y - ny + ay * dt * dt
    t = t + dt
    
    nx = x
    ny = y
    x = px
    y = py
    
    height_km = (h(x, y)-R)/np.float64(1000.0)
    if (round(height_km) - round(prevH) < 0):
        print "V = " + str(v / np.float64(1000.0)) + "    H = " + str(height_km) + "   dv = " + str((v - prevV)*np.float64(1000))
        
    if  (x > 0) and (nx < 0) and (y > 0):
        i += 1
        print str(i) + "  V = " + str(v / np.float64(1000.0)) + "   H = " + str(height_km) + "   dv = " + str((v - prevV)*np.float64(1000))
        print "t = " + str(t)
        print "x = " + str(x)
        print "y = " + str(y-R)
    
    if t > 100000:
        print "t = " + str(t)
        print "x = " + str(x)
        print "y = " + str(y-R)
    
    prevH = height_km
    prevV = v


# 1000 kg and 1 m2  
# V = 7.84075641403        H = 107.499923762
# V = 7.84082969302 -MAX   H = 106.49993188
# V = 7.84081902724        H = 105.499979367

# 1 g of ice
#V = 7.81889065889    H = 138.499844548
#V = 7.81890835209    H = 137.499831885
#V = 7.81887793463    H = 136.499789166


