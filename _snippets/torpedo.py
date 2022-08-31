import random
import math
from matplotlib import pyplot as plt

"""
https://zen.yandex.ru/media/id/5a630d2c9b403c5442578563/tvorcy-mashin-pervoe-primenenie-giroskopa-ego-vstavili-v-torpedu-chtoby-ona-popadala-vcel--5b7bd821e1552600a9c3b119

Первый опытный образец был готов через несколько месяцев. В Адриатике выпустили 2 торпеды, с гироскопом внутри и без него. Торпеда без гироскопа на пути в 1 километр ушла в сторону от цели на 250 метров.

http://weapons-world.ru/books/item/f00/s00/z0000011/st006.shtml

В современных зарубежных торпедах точность хода по направлению зависит от пройденной дистанции и составляет ±1 % на дистанциях до 10000 м. Точность хода по глубине у торпед со скоростью до 55 уз, предназначенных для применения по надводным кораблям, составляет приблизительно ±1 м от заданной глубины

Электрическая ЭСУ по сравнению с воздушной тепловой имеет преимущества: ... во время движения она более устойчиво держится на заданном курсе, так как (в отличие от тепловой) при движении не изменяется ни масса, ни положение центра тяжести (не расходуется воздух, вода, керосин). 

Траектории движения торпед, управляемых автономными приборами
http://weapons-world.ru/books/item/f00/s00/z0000011/st010.shtml

"""

def step(x, y, angle):
  x += math.cos(angle/180*math.pi)
  y += math.sin(angle/180*math.pi)
  return x, y

def run_1km(k):
  angle = 0
  x = y = 0
  while x < 1000:
    angle += (random.random() - 0.5) * k
    x, y = step(x, y, angle)
  return abs(y)

def circle_run(length, curvative, k):
  angle = 0
  x = y = 0
  result = [(x, y)]
  for i in range(length):
    angle += curvative(i) if callable(curvative) else curvative
    angle += (random.random() - 0.5) * k
    x, y = step(x, y, angle)
    result.append((x, y))
  return result

random.seed(1)
runs = [run_1km(3.5) for _ in range(1000+1)]
runs.sort()
print(runs[0], runs[500], runs[-1])


plt.plot(*zip(*circle_run(10_000, 0.3, 3.5)))
plt.show()

plt.plot(*zip(*circle_run(30_000, 0.1, 3.5)))
plt.show()

plt.plot(*zip(*circle_run(10_000, lambda n: 0.3 - n/30_000, 3.5)))
plt.show()