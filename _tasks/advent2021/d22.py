"""
one cube per integer 3-dimensional coordinate (x,y,z)
Each cube can be either on or off; at the start of the reboot process, they are all off
"""

#data = [line.strip() for line in open('test22.txt').readlines()]
data = [line.strip() for line in open('input22.txt').readlines()]

def dot_in_cube(dot, cube):
    x, y, z = dot
    (x1, x2), (y1, y2), (z1, z2) = cube
    if x1 <= x < x2:
        if y1 <= y < y2:
            if z1 <= z < z2:
                return True
    return False

def cube_volume(cube):
    (x1, x2), (y1, y2), (z1, z2) = cube
    return (x2-x1) * (y2-y1) * (z2-z1)

def cubes_volume(cubes):
    return sum([cube_volume(cube) for cube in cubes])

def merge_intervals(a, b):
    a1, a2 = a
    b1, b2 = b
    v = set([a1, a2, b1, b2])
    if len(v) == 3:
        return (min(v), max(v))
    return None

def merge_cubes(cube1, cube2):
    x1, y1, z1 = cube1
    x2, y2, z2 = cube2
    if x1 == x2 and y1 == y2:
        v = merge_intervals(z1, z2)
        if v:
            return (x1, y1, v)
    if x1 == x2 and z1 == z2:
        v = merge_intervals(y1, y2)
        if v:
            return (x1, v, z1)
    if z1 == z2 and y1 == y2:
        v = merge_intervals(x1, x2)
        if v:
            return (v, y1, z1)
    return None


def split_cubes(cube1, cube2, cube2_on):  # cube1 always on, we split only cube1
    (x1, x2), (y1, y2), (z1, z2) = cube1
    (x1_, x2_), (y1_, y2_), (z1_, z2_) = cube2
    xs = [x1, x2, x1_, x2_]
    ys = [y1, y2, y1_, y2_]
    zs = [z1, z2, z1_, z2_]
    xs.sort()
    ys.sort()
    zs.sort()
    result = []
    for xx1, xx2 in zip(xs[:-1], xs[1:]):
        if xx1 == xx2:
            continue
        for yy1, yy2 in zip(ys[:-1], ys[1:]):
            if yy1 == yy2:
                continue
            for zz1, zz2 in zip(zs[:-1], zs[1:]):
                if zz1 == zz2:
                    continue
                dot = (xx1, yy1, zz1)
                res_in_cube1 = dot_in_cube(dot, cube1)
                current_cube_on = res_in_cube1
                if dot_in_cube(dot, cube2):
                    current_cube_on = cube2_on
                if res_in_cube1 and current_cube_on:
                    result.append(((xx1, xx2), (yy1, yy2), (zz1, zz2)))
    # merge it back
    if len(result) < 2:
        return result  # 0 or 1, nothing to merge
    while True:
        new_result = []
        i = 0
        while True:
            if i == len(result):
                break
            cube1 = result[i]
            if (i+1) == len(result):
                new_result.append(cube1)
                break
            cube2 = result[i+1]
            v = merge_cubes(cube1, cube2)
            if v:
                #assert cube_volume(v) == (cube_volume(cube1) + cube_volume(cube2))
                new_result.append(v)
                i += 2
            else:
                i += 1
                new_result.append(cube1)
        #assert cubes_volume(new_result) == cubes_volume(result)
        if len(result) == len(new_result):
            return result
        result = new_result

def parse_line(line):
    # on x=16383..101554,y=4615..83635,z=-44907..18747
    on = line.startswith('on')
    cube = []
    for v in line.split(' ')[1].split(','):
        a, b = v.split('=')[1].split('..')
        a = int(a)
        b = int(b)
        assert a<=b
        cube.append((a, b+1))
    return (on, cube)

cubes = []
for line in data:
    print(len(cubes), line)
    on, new_cube = parse_line(line)
    new_cubes = []
    extra = [new_cube] if on else []
    for cube in cubes:
        res = split_cubes(cube, new_cube, on)
        new_cubes += res
        new_extra = []
        for cube2 in extra:
            new_extra += split_cubes(cube2, cube, False)
        extra = new_extra
    print(f'{len(new_cubes)} {len(extra)}')
    cubes = new_cubes + extra


print('task 1', 503864)

print(f'{len(cubes)=}')
print('task 2', cubes_volume(cubes))
# time 192 sec
