import numpy as np

#data = [line.strip() for line in open('test22.txt').readlines()]
data = [line.strip() for line in open('input22.txt').readlines()]


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


def convert(a,b, arr):
    return np.searchsorted(arr, a), np.searchsorted(arr, b)


xs = set()
ys = set()
zs = set()
for line in data:
    _, new_cube = parse_line(line)
    (x1, x2), (y1, y2), (z1, z2) = new_cube
    xs.add(x1)
    xs.add(x2)
    ys.add(y1)
    ys.add(y2)
    zs.add(z1)
    zs.add(z2)

xs = np.array(list(xs))
xs.sort()
ys = np.array(list(ys))
ys.sort()
zs = np.array(list(zs))
zs.sort()

shape = (len(xs)-1, len(ys)-1, len(zs)-1)
state = np.zeros(shape, dtype=np.int8)
for line in data:
    on, new_cube = parse_line(line)
    on = np.int8(1 if on else 0)
    (x1, x2), (y1, y2), (z1, z2) = new_cube
    x1, x2 = convert(x1, x2, xs)
    y1, y2 = convert(y1, y2, ys)
    z1, z2 = convert(z1, z2, zs)
    state[x1:x2,y1:y2,z1:z2] = on

yzss = np.outer(np.diff(ys), np.diff(zs))

volume = 0
for ix in range(len(xs)-1):
    v = np.einsum('ij,ij', yzss, state[ix])
    if v:
        volume += (xs[ix+1]- xs[ix]) * v

print('task 2', volume)  # 1255547543528356

# 1 second per run
