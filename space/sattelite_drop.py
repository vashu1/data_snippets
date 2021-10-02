import math

dt = 0.01 # seconds

G = 6.673848e-11
M = 5.97219e24

# satellite
m = 1000.0 # kg
s = 1.0 # m2

# Earth
R = 6.371e6 # meters
H = 150 * 1000.0 # meters

def h(x, y):
    return math.sqrt(x * x + y * y)
    
def g(x, y):
    h0 = h(x, y)
    return G * M / (h0 * h0)

# valid below 180 km
# Source: http://www.spaceacademy.net.au/watch/debris/atmosmod.htm
a0 = +7.001985e-2
a1 = -4.336216e-3
a2 = -5.009831e-3
a3 = +1.621827e-4
a4 = -2.471283e-6
a5 = +1.904383e-8
a6 = -7.189421e-11
a7 = +1.060067e-13
def dens(x, y):
    h0 = (h(x, y) - R) / 1000.0
    if h0 < 0 or h0 > 180:
        raise ValueError("Height must be in 0-180 km range!")
    appr = a0 + h0 * (a1 + h0 * (a2 + h0 * (a3 + h0 * (a4 + h0 * (a5 + h0 * (a6 + h0 * a7))))))
    return math.exp(appr * math.log(10)) 

# test `dens()`
#print dens(0, R +   0)
#print (dens(0, R +  50 *1000.0) - 1.03e-3) / 1.03e-3
#print (dens(0, R +  80 *1000.0) - 1.85e-5) / 1.85e-5
#print (dens(0, R + 100 *1000.0) - 5.55e-7) / 5.55e-7
#print (dens(0, R + 150 *1000.0) - 2.0e-9) / 2.0e-9
#print (dens(0, R + 200 *1000.0) - 2.52e-10) / 2.52e-10

V =  math.sqrt(G * M / (R + H)) # m/s

nx = 0.0
ny = R + H

x = nx + dt * V
y = ny - g(nx, ny) * dt * dt / 2

t = 0.0 # seconds
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
    afriction = s / m * dens(x, y) * v * v 
    axf = - y1 * afriction
    ayf = + x1 * afriction
    
    ax = axg + axf
    ay = ayg + ayf
    px = 2 * x - nx + ax * dt * dt
    py = 2 * y - ny + ay * dt * dt
    t = t + dt
    
    nx = x
    ny = y
    x = px
    y = py
    
    height_km = (h(x, y)-R)/1000.0
    if (round(height_km) - round(prevH) < 0):
        print "V = " + str(v / 1000.0) + "    H = " + str(height_km) + "   dv = " + str((v - prevV)*1000)
        
    if (x > 0) and (nx < 0) and (y > 0):
        i += 1
        print str(i) + "  V = " + str(v / 1000.0) + "   H = " + str(height_km) + "   dv = " + str((v - prevV)*1000)
    
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
