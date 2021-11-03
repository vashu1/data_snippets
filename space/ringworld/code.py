import math
from typing import Tuple, List
import scipy  # type: ignore
import matplotlib.pyplot as plt  # type: ignore

#TODO rewrite to numpy vectors?

SUN_MASS = 1.989e30

# https://ru.wikipedia.org/wiki/%D0%9C%D0%B8%D1%80-%D0%9A%D0%BE%D0%BB%D1%8C%D1%86%D0%BE#%D0%9F%D0%B0%D1%80%D0%B0%D0%BC%D0%B5%D1%82%D1%80%D1%8B_%D0%9A%D0%BE%D0%BB%D1%8C%D1%86%D0%B0
RING_MASS = 2e27  # kg
RING_RADIUS = 1.53e11  # m
RING_WIDTH = 1.6e9  # m

INTEGRATION_TOP_STEPS = 720

G = 6.67e-11

SPLIT_RECT_REL_THRESHOLD = 0.1

Point = Tuple[float, float, float]
Rect = Tuple[Point, Point, Point, Point]

def avg(a: float, b: float) -> float:
    return (a+b)/2


def middle_point(p1: Point, p2: Point) -> Point:
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    return avg(x1, x2), avg(y1, y2), avg(z1, z2)


def rect_center(rect: Rect) -> Point:
    p1, p2, p3, p4 = rect
    p12 = middle_point(p1, p2)
    p34 = middle_point(p3, p4)
    return middle_point(p12, p34)


def split_rect(rect: Rect) -> List[Rect]:  # splits 1 rect in 4
    p1, p2, p3, p4 = rect
    p12 = middle_point(p1, p2)
    p23 = middle_point(p2, p3)
    p34 = middle_point(p3, p4)
    p41 = middle_point(p4, p1)
    pcenter = rect_center(rect)
    return [
        (p1, p12, pcenter, p41),
        (p12, p2, p23, pcenter),
        (p41, pcenter, p34, p4),
        (pcenter, p23, p3, p34),
    ]


def distance_square(p1: Point, p2: Point = (0, 0, 0)) -> float:
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    return (x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2


def distance(p1: Point, p2: Point = (0, 0, 0)) -> float:
    return math.sqrt(distance_square(p1, p2))


def sum_v(*vectors) -> Point:
    return tuple(map(sum, zip(*vectors)))  # type: ignore


def integrate_rect(rect: Rect, mass: float, point: Point) -> Point:
    points = list(rect) + [rect_center(rect)]
    distances = [distance(point, p) for p in points]
    max_distance = max(distances)
    min_distance = min(distances)
    if max_distance < 1:
        return 0, 0, 0  # point is inside ring so we stop recursion
    rel = (max_distance - min_distance) / min_distance
    if rel > SPLIT_RECT_REL_THRESHOLD:
        return sum_v(*[integrate_rect(rect2, mass/4, point) for rect2 in split_rect(rect)])
    else:
        center = rect_center(rect)
        length = G * mass / distance_square(center, point)
        dist = distance(point, center)
        k = length / dist
        x1, y1, z1 = center
        x2, y2, z2 = point
        return (x1-x2)*k,(y1-y2)*k,(z1-z2)*k


def integrate(point: Point) -> Point:
    degree_step = 360/INTEGRATION_TOP_STEPS
    acc = []
    for i in range(INTEGRATION_TOP_STEPS):
        degree = i * degree_step
        radians = math.radians(degree)
        radians2 = math.radians(degree + degree_step)
        z = RING_WIDTH / 2
        y1 = math.sin(radians) * RING_RADIUS
        x1 = math.cos(radians) * RING_RADIUS
        y2 = math.sin(radians2) * RING_RADIUS
        x2 = math.cos(radians2) * RING_RADIUS
        rect = (
            (y1, x1, +z),
            (y1, x1, -z),
            (y2, x2, -z),
            (y2, x2, +z),
        )
        acc.append(integrate_rect(rect, RING_MASS/INTEGRATION_TOP_STEPS, point))
    return sum_v(*acc)


"""
print(integrate((0,0,0)))
print(integrate((RING_RADIUS - 1,0,0)))
print(integrate((RING_RADIUS + 1,0,0)))
print(integrate((RING_RADIUS - 1e3,0,0)))
print(integrate((RING_RADIUS - 1e6,0,0)))
print(integrate((RING_RADIUS - 1e9,0,0)))
print(integrate((RING_RADIUS,0,0)))

((9.021438555656458e-24, 4.301339185275744e-23, 0.0), 4.394926884821117e-23)
((0.0005201188861631926, -1.2231449291664267e-14, 5.293955920339377e-23), 0.0005201188861631926)
((0.0005301388183980967, 1.7071471355106674e-17, -1.0819522412193602e-19), 0.0005301388183980967)
((0.0002298074280754826, 3.927428732983399e-19, 1.6543612251060553e-21), 0.0002298074280754826)
"""

# print(G*SUN_MASS/(RING_RADIUS**2))  # 0.0056

# https://znanija.com/task/20885377
# Ускорение свободного падения, сообщаемое Солнцем: 6*10⁻³ м/с²
# https://reshak.ru/otvet/reshebniki.php?otvet=30/c1&predmet=myakishev10   6 mm/s2

# earth - 6400 10 m/s2  * 100  0.64 Mkm  0.1 mm/s2

"""
def sun_satellite_v(height: float) -> float:
    r = RING_RADIUS - height
    sun_g = G * SUN_MASS / (r ** 2)
    return math.sqrt(sun_g * r)
"""

def satellite_gv(height: float) -> Tuple[float, float]:
    assert height > 0  # otherwise fix code to account for ring gravitation direction
    r = RING_RADIUS - height
    sun_g = G * SUN_MASS / (r ** 2)
    ring_g_v = integrate((r, 0, 0))
    g = sun_g - distance(ring_g_v)
    satellite_v = math.sqrt(g * r)
    return g, satellite_v


def stability(height: float, dh: float = 1) -> bool:  # height relative to ring
    g, satellite_v = satellite_gv(height)
    g2, satellite_v2 = satellite_gv(height - dh)  # rise with positive dh, height above ring is lower
    #
    ped = (g+g2)/2*dh # potential energy differential
    ke = satellite_v**2 / 2 # kinetic energy
    ke2 = satellite_v2 ** 2 / 2
    result = ke < (ke2 + ped)
    if dh < 0:
        result = not result
    return result

"""
print(satellite_gv(1e6))
print(satellite_gv(1e6+1e3))

print(stability(1e6))
print('---')
print(stability(1e7/3))
print(stability(1e9))
print('---')
print(stability(3e9))
"""

def find_boundary(h1, h2, dh = 1):
    h12 = avg(h1, h2)
    if abs(h2 - h1) < dh:
        return h12
    s1 = stability(h1)
    s12 = stability(h12)
    s2 = stability(h2)
    assert s1 != s2
    if s1 == s12:
        return find_boundary(h12, h2, dh)
    else:
        return find_boundary(h1, h12, dh)
"""
print('boundary')
print(find_boundary(1e6, 1e7/3))  # 2_206_939.3396377563
print(find_boundary(1e9, 3e9))  # 2_629_883_170.5935297
"""

"""
О спутниках Мира Кольца.

Кольцо имеет собственную гравитацию - порядка половины мм/с2. Это на порядок слабее притяжения Солнца, проблема в том что гравитация Кольца меняется быстрее солнечной.

Пусть спутник вращается на круговой гелиоцентрической орбите в плоскости Кольца. Очевидно, что на большом расстоянии от Кольца гравитация Солнца доминирует и орбита стабильна.

Но что если спутник вращается на небольшой высоте над внутренней стороной? Тогда если орбита чуть поднимется то скорость спутника уменьшится. Но Кольцо ослабит гравитацию Солнца сильнее чем квадратичное убывание и ценробежная сила не сбалансирует гравитацию - орбита станет нестабильной.

Интересно что если мы спустимся на очень небольшую высоту над поверхностью, то производная гравитации Кольца станет околонулевой из-за его плоской формы и дестабилизирующий эффект перестанет работать. 

Расчет показывает что регион нестабильности проходит с высоты 2.207 км до 2,63 миллионов км. (спутник может врашаться и на орбите в этой зоне, с постоянной работой стабилизирующих двигателей)

Таким образом эффект позволяет использовать низкие орбиты, но удобные для быстрой ретрансляции/наблюдения за погодой/и тп тд орбиты средней высоты требуют стабилизацию.

Ситуация осложняется если мы хотим отклониться от плоскости вращения Кольца (чтобы рассмотреть пристенные районы получше). Нетрудно прикинуть что потенциальная энергия гравитации Кольца для спутника на низкой орбите будет порядка 200 кДж, достаточно чтобы нарастить скорость спутника на 0.5 км в секунду и изменить его высоту на миллионы км.

https://worldbuilding.stackexchange.com/questions/79716/stable-ringworld-interactivity-with-other-solar-system-objects
helical motion around a ringworld

physics demonstration of charged droplets spiralling around a charged knitting needle 


5e-4 * (1e6**2) / 2 / 1000   10 days to "fall"
V = 5e-4 * 1e6 = 500 м/с
"""

def dg(height: float, dh: float = 1) -> float:
    assert height > 0  # otherwise fix code to account for ring gravitation direction
    r = RING_RADIUS - height
    sun_g = G * SUN_MASS / (r ** 2)
    ring_g = distance(integrate((r, 0, 0)))
    sun_g2 = G * SUN_MASS / ((r-dh) ** 2)
    ring_g2 = distance(integrate(((r-dh), 0, 0)))
    return (sun_g2 - ring_g2) - (sun_g - ring_g)


"""
print(dg(1e6))
print(dg(1e7/3))
print(dg(1e7))
print(dg(1e10))
"""


def ring_side_potential(points=100, height = 1e6) -> float:
    r = RING_RADIUS - height
    acc = []
    for i in range(points):
        z = RING_WIDTH / 2 * i / (points - 1)
        ring_g = integrate((r, 0, z))
        _, _, az = ring_g
        acc.append((az, z))
    return scipy.integrate.simps(*zip(*acc))

"""
print('ring_side_potential:')
print(ring_side_potential(points=10))  # -206998
print(ring_side_potential(points=30))  # -1 94531
print(ring_side_potential(points=100))  # -192228
"""

def scalar(v1: Point, v2: Point) -> float:
    x1, y1, z1 = v1
    x2, y2, z2 = v2
    return x1*x2 + y1*y2 + z1*z2

def mul_v(v: Point, a: float) -> Point:
    x, y, z = v
    return a*x, a*y, a*z


def unit(v: Point) -> Point:
    d = distance(v)
    return mul_v(v, 1/d)


def rotate_z(p: Point, alpha_rad: float) -> Point:
    x, y, z = p
    cs = math.cos(alpha_rad)
    sn = math.sin(alpha_rad)
    x = x * cs + y * sn
    y = y * cs - x * sn
    return x, y, z


def leapfrog(time: float, height: float, z: float, dt: float = 1e4) -> List[Point]:
    def a(p):
        ring_g_v = integrate(p)
        sun_g = G * SUN_MASS / distance_square(p)
        sun_g_v = mul_v(unit(p), -sun_g)
        a = sum_v(ring_g_v, sun_g_v)
        #print(a)
        return a
    #TODO move out, pass p,v as params
    r = RING_RADIUS - height
    ring_g_v = integrate((r, 0, z))
    vector = (r, 0, z)
    ring_g = scalar(unit(vector), ring_g_v)
    sun_g = G * SUN_MASS / distance_square(vector)
    g = sun_g - ring_g
    satellite_v = math.sqrt(g * distance(vector))  #TODO add k multiplicator
    print(sun_g - ring_g, sun_g, ring_g)
    print(satellite_v)
    points = []
    # https://en.wikipedia.org/wiki/Leapfrog_integration
    v = (0., satellite_v, 0.)
    p = (r, 0., z)
    points.append(p)
    t = 0.
    a_prev = a(p)
    while t <= time:
        vdt = mul_v(v, dt)
        p1 = sum_v(p, vdt, mul_v(a_prev, (dt**2) / 2))
        a_cur = a(p1)
        print('a', distance(a_cur), distance(v)**2/distance(p), distance(a_cur) - distance(v)**2/distance(p))
        v1 = sum_v(v, mul_v(sum_v(a_prev, a_cur), dt / 2))
        print('v', v1)
        #print('-', v, sum_v(a_prev, a_cur))
        #print('v1', distance(v1), v1)
        # rotate vectors to keep y close to 0
        for i in range(2):  #TODO ? 1
            d = distance(p1)
            alpha = p1[1] / d
            p1 = rotate_z(p1, alpha)
            v1 = rotate_z(v1, alpha)
            a_cur = rotate_z(a_cur, alpha)
        #assert abs(p1[1]) < 1
        # save
        points.append(p1)
        v = v1
        p = p1
        a_prev = a_cur
        t += dt
    return points


def draw_orbit(points: List[Point]) -> None:
    _, _, zs = zip(*points)
    xs = [RING_RADIUS - distance(p) for p in points]
    plt.scatter(xs, zs)
    plt.plot(xs, zs)
    print('draw_orbit')
    print(zs)
    print(xs)
    #TODO add ring line
    plt.show()

points = leapfrog(time=9e5, height=1e5, z=0, dt=3e3)
draw_orbit(points)

# https://youtu.be/d1sr6aVzW9M?t=39   NASA astronauts performing gymnastics on board of the Skylab

# count iterations in integrate

# satellite with solar sail
# print(integrate((RING_RADIUS-1e6, 0, RING_WIDTH/2)))  # -0.001280277154359685
# print(integrate((RING_RADIUS-1e6, 0, 0)))
