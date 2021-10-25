import math

# При работе сопла Лаваля в непустой среде
# https://ru.wikipedia.org/wiki/%D0%A1%D0%BE%D0%BF%D0%BB%D0%BE_%D0%9B%D0%B0%D0%B2%D0%B0%D0%BB%D1%8F#%D0%A4%D1%83%D0%BD%D0%BA%D1%86%D0%B8%D0%BE%D0%BD%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5_%D0%B2_%D1%81%D1%80%D0%B5%D0%B4%D0%B5
# срыву сверхзвукового

# Обычно на орбиту выходит за 8-9 минут.

EARTH_RADIUS = 6_378_000
G = 9.81

LEO_H = 300_000


def flatten(lst):
    return [elem for sublist in lst for elem in sublist]


def g(y):
    factor = (EARTH_RADIUS + y) / EARTH_RADIUS
    factor **= 2
    return G / factor


def centrifugal(y, vx):
    return vx**2 / (EARTH_RADIUS + y)


"""
TODO

check OUT of fuel
add per second iteration in apply()

stages
expansion_factor of nozzle
atmosphere drag - check thrust vector
max allowed acceleration
"""
class Rocket2D:
    # state
    x, y = 0, 0
    vx, vy = 0, 0
    weight = 1
    # details
    empty_weight = 0.1
    max_a = 30
    isp = 300
    min_dt = 1
    def __init__(self):  # , expansion_factor=3
        pass
    # trajectory   (dt, thrust_x, thrust_y) in ratio from max_consumption, eg (1,1) - max thrust at 45, (0,1) max vertically
    def apply(self, trajectory):
        if isinstance(trajectory, type(np.array([]))):  # TODO fix type
            trajectory = [trajectory[indx:indx + 3] for indx in range(0, len(trajectory), 3)]
        saved = []
        t = 0
        saved.append((t, self.weight, self.x, self.y, self.vx, self.vy))
        for point in trajectory:
            # apply
            step_time, thrust_x, thrust_y = point
            if step_time == 0:
                continue
            while step_time > 0:
                dt = min(self.min_dt, step_time)
                step_time -= self.min_dt
                #
                thurst = math.sqrt(thrust_x**2 + thrust_y**2)
                if thurst > 2:
                    thurst = 2
                max_consumption = self.max_a * self.weight / (dt * self.isp * 10)  # if (thurst==1) consumption = max_a
                consumption = thurst * max_consumption * dt
                if thurst > 1:  # to keep smooth but to make thrust>1 bad
                    thurst = 1 - thurst
                a = thurst * max_consumption * dt * self.isp * 10 / self.weight
                if a > self.max_a:
                    if a > self.max_a*2:
                        a = self.max_a*2
                    a = self.max_a*2 - a
                ax, ay = a * thrust_x, a * thrust_y
                ay += centrifugal(self.y, self.vx) - g(self.y)
                # modify state
                self.weight -= consumption
                self.x += self.vx + dt**2 * ax / 2
                self.y += self.vy + dt**2 * ay / 2
                self.vx += ax
                self.vy += ay
                t += dt
            # save
            saved.append((t, self.weight, self.x, self.y, self.vx, self.vy))
        return saved

#Rocket2D().apply([(1, 0, 1)]*2)

import numpy as np
from scipy.optimize import minimize


trajectory = [(0.999,0.001,0.999)for i in range(90)] + [(0.999,0.999,0.001) for i in range(280)]
trajectory = [(90,0,1)] + [(280,1,0)]
points = Rocket2D().apply(trajectory)
last_point = points[-1]
dt, weight, x, y, vx, vy = last_point
print(f'{dt=} weight {round(weight,2)} P {round(x/1000)} {round(y/1000)} V= {round(vx/1000,1)} {round(vy/1000,1)}')

count = 0
def f(trajectory):
    points = Rocket2D().apply(trajectory)
    last_point = points[-1]
    dt, weight, x, y, vx, vy = last_point
    vertical_a = centrifugal(y, vx) - g(y)
    res = ((LEO_H - y)/10_000)**2 + vertical_a ** 2 + ((1 - weight) * 10) ** 2
    #res = max(((LEO_H - y) / 10_000) ** 2, vertical_a ** 2, ((1 - weight) * 10) ** 2)
    #print('a', vertical_a, 'H', LEO_H - y)
    global count
    count += 1
    if count % 1000 == 0:
        print(f'count={count/1000}K f() {res=}')
    return res

f(res.x)
Rocket2D().apply(res.x)

x0 = np.array(flatten(trajectory))
res = minimize(f, x0, method='nelder-mead',options={'xatol': 1e-9, 'disp': True})
#

x0 = np.array(flatten(trajectory))
res = minimize(f, x0, method='BFGS',options={'xatol': 1e-9, 'disp': True})


res = minimize(f, x0, method='SLSQP', options={'ftol': 1e-1, 'disp': True})

split in half?


trajectory = [(90,0,1)] + [(280,1,0)]
trajectory(trajectory)