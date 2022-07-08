# MSISE-90 Model of Earth's Upper Atmosphere http://www.braeunig.us/space/atmos.htm
from scipy.interpolate import interp1d
import math

points = {  # height in km to density
    0: 1.17E+000,
    20: 9.49E-002,
    40: 4.07E-003,
    60: 3.31E-004,
    80: 1.68E-005,
    100: 5.08E-007,
    120: 1.80E-008,
    140: 3.26E-009,
    160: 1.18E-009,
    180: 5.51E-010,
    200: 2.91E-010,
    220: 1.66E-010,
    240: 9.91E-011,
    260: 6.16E-011,
    280: 3.94E-011,
    300: 2.58E-011,
    320: 1.72E-011,
    340: 1.16E-011,
    360: 7.99E-012,
    380: 5.55E-012,
    400: 3.89E-012,
    420: 2.75E-012,
    440: 1.96E-012,
    460: 1.40E-012,
    480: 1.01E-012,
    500: 7.30E-013,
    520: 5.31E-013,
    540: 3.88E-013,
    560: 2.85E-013,
    580: 2.11E-013,
    600: 1.56E-013,
    620: 1.17E-013,
    640: 8.79E-014,
    660: 6.65E-014,
    680: 5.08E-014,
    700: 3.91E-014,
    720: 3.04E-014,
    740: 2.39E-014,
    760: 1.90E-014,
    780: 1.53E-014,
    800: 1.25E-014,
    820: 1.03E-014,
    840: 8.64E-015,
    860: 7.32E-015,
    880: 6.28E-015,
    900: 5.46E-015,
}

f = interp1d(*zip(*points.items()))
def get_density(height_km: float) -> float:
    return f(height_km)


def dens(x, y):
    height_km = (h(x, y) - R) / 1000
    return get_density(height_km)

dt = 1 # seconds

G = 6.673848e-11
M = 5.97219e24

# satellite / debris
m = 0.003  # kg
s = 1e-4  # m2
height = 400
extra_v = 135/4  # to elliptic orbit - 135 m/s means apogee minus perigee = about 500 km

# Earth
R = 6.371e6 # meters
H = height * 1000.0 # meters

def h(x, y):
    return math.sqrt(x * x + y * y)

def g(x, y):
    h0 = h(x, y)
    return G * M / (h0 * h0)

V =  math.sqrt(G * M / (R + H)) + extra_v  # m/s

nx = 0.0
ny = R + H

x = nx + dt * V
y = ny - g(nx, ny) * dt * dt / 2

t = 0.0 # seconds
i = 0
prevH = H
prevV = V

apogee = height, V
perigee = None, None
n = 0

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

    height_km = (h(x, y) - R) / 1000.0
    if nx <= 0 and x>0:
        if n % 100 == 0:
            print('perigee', height_km, v)
            print('diff perigee h', round((height_km - apogee[0]) * 1000, 1))
        apogee = height_km, v
    if nx >=0 and x<0:
        n += 1
        if n % 100 == 0:
            print('apogee', height_km, v)
            if perigee[0]:
                print('diff apogee h', round((height_km - perigee[0])*1000, 1))
            perigee = height_km, v
            print('N', n, 'day', round(t/3600/24, 1))

    nx = x
    ny = y
    x = px
    y = py

    prevH = height_km
    prevV = v

"""
average sun activity

-75.4 m with round orbit

with +500 km elliptic

perigee 399.9930536250705 7807.3332822808425
diff perigee h -2.3
apogee 898.3345619226778 7272.10559181261
diff apogee h -32.6

>>> -32.6/-2.3
14.173913043478263

"""

"""
https://habr.com/ru/company/timeweb/blog/595577/
По состоянию на январь 2019 года на орбите находилось 128 000 000 обломков размером 
менее 1 см, около 900 000 обломков размером 1–10 см и около 34 000 обломков размером 
более 10 см. 

По оценкам ЕКА, на околоземной орбите находится не менее 36 500 обломков размером более 
10 сантиметров в ширину, 1 миллион объектов от от 1 до 10 см в поперечнике и более 
300 миллионов объектов размером от 1 мм до 1 см.


"""