
# example target area: x=20..30, y=-10..-5
# an initial velocity of 6,9 is the best you can do, causing the probe to reach a maximum y position of 45

# input target area: x=150..193, y=-136..-86

# Due to drag, the probe's x velocity changes by 1 toward the value 0; that is, it decreases by 1 if it is
# greater than 0, increases by 1 if it is less than 0, or does not change if it is already 0.
# Due to gravity, the probe's y velocity decreases by 1

# example
target = ((20, 30), (-10,-5))  # x1x2, y1y2
# input
#target = ((150, 193), (-136,-86))

def run(vx, vy):
    x = 0
    y = 0
    max_height = None
    while True:
        if (max_height is None) or (y > max_height):
            max_height = y
        if target[1][0] <= y <= target[1][1]:
            if target[0][0] <= x <= target[0][1]:  # reached target
                return max_height
        if  y < target[1][0]:
            return None
        x += vx
        y += vy
        vx -= 1
        if vx < 0:
            vx = 0
        vy -= 1

v = []
for vx in range(1, 400):
    for vy in range(-250, 250):
        res = run(vx, vy)
        if not res is None:
            v.append((res, vx, vy))

v.sort(key=lambda x: x[0], reverse=True)
print(v[:5])
print(len(v))
print(len(set([(x[1],x[2]) for x in v])))