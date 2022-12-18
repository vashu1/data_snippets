from utils import *
from collections import defaultdict, Counter, deque

input_test = """2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5"""
input_test = input_test.split('\n')

input_full = open('d18.txt').readlines()

input = [l.strip() for l in input_full]

DZ = 2
SZ = 20+2*DZ
cube = [[[0 for _ in range(SZ)] for _ in range(SZ)] for _ in range(SZ)]


def parse(line):
    return list(map(lambda s: int(s)+DZ, line.split(',')))


data = [parse(line) for line in input]
xs, ys, zs = zip(*data)

#print(f'{min(xs)=} {max(xs)=} {min(ys)=} {max(ys)=} {min(zs)=} {max(zs)=}')

for x, y, z in data:
    cube[x][y][z] = 1


def count_air():
    s = 0
    for x in range(DZ, 19+1+DZ):
        for y in range(DZ, 19+1+DZ):
            for z in range(DZ, 19+1+DZ):
                if cube[x][y][z]:
                    s += 6
                    s -= cube[x+1][y][z]
                    s -= cube[x-1][y][z]
                    s -= cube[x][y+1][z]
                    s -= cube[x][y-1][z]
                    s -= cube[x][y][z+1]
                    s -= cube[x][y][z-1]
    return s


print(count_air())

# PART II


def replace(a, b):
    for x in range(0, SZ):
        for y in range(0, SZ):
            for z in range(0, SZ):
                if cube[x][y][z] == a:
                    cube[x][y][z] = b


replace(0, -1)

# fill outside of cube
stack = [(1, 1, 1)]  # outside of cube
while stack:
    x, y, z = stack.pop()
    if cube[x][y][z] == -1:
        if x == 0 or y == 0 or z == 0:
            continue
        if x == SZ - 1 or y == SZ - 1 or z == SZ - 1:
            continue
        cube[x][y][z] = 0
        stack.append((x+1, y, z))
        stack.append((x-1, y, z))
        stack.append((x, y+1, z))
        stack.append((x, y-1, z))
        stack.append((x, y, z+1))
        stack.append((x, y, z-1))

replace(-1, 1)

print(count_air())