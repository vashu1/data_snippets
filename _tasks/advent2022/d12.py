from utils import *
from collections import defaultdict, Counter, deque
from heapq import heappush, heappop

input_test = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""
input_test = input_test.split('\n')

input_full = open('d12.txt').readlines()

input = [l.strip() for l in input_full]

# the elevation of the destination square can be at most one higher than the elevation of your current square;
# that is, if your current elevation is m, you could step to elevation n, but not to elevation o.
# (This also means that the elevation of the destination square can be much lower than the elevation of your current square.)

# find S E

h = len(input)
w = len(input[1])

start_pos = ''.join(input).find('S')
start_pos = (start_pos % w, start_pos // w)
end_pos = ''.join(input).find('E')
end_pos = (end_pos % w, end_pos // w)

input2 = [str(input[i]) for i in range(h)]
input = [list(s) for s in input]
input[start_pos[1]][start_pos[0]] = 'a'
input[end_pos[1]][end_pos[0]] = 'z'

visited = set([start_pos])
paths = []
heappush(paths, (0, start_pos, []))

while paths:
    steps, (x, y), pt = heappop(paths)
    #print('--',steps, x, y)
    for i, j, m in [(1,0, '>'), (-1,0, '<'), (0,1, 'v'), (0,-1, '^')]:
        if x + i >= 0 and x +i < w:
            if y + j >= 0 and y + j < h:
                if (x+i, y+j) in visited:
                    continue
                # check we can step
                v0 = input[y][x]
                v1 = input[y+j][x+i]
                #print(v0, v1)
                if ord(v1) - ord(v0) > 1:
                    continue
                if (x+i, y+j) == end_pos:
                    print('answer', steps + 1)
                    print(pt)
                    paths = []
                    break
                #print('ord', ord(v1) - ord(v0))
                #input2[y+j] = input2[y+j][:x+i] + m + input2[y+j][x+i+1:]
                visited.add((x+i, y+j))
                heappush(paths, (steps+1, (x+i, y+j), list(pt) + [v1]))  # (x+i, y+j, m)

#for i in range(h):
#    print(input2[i])

# not 427

def get_route(start_pos):
    visited = set([start_pos])
    paths = []
    heappush(paths, (0, start_pos, []))
    while paths:
        steps, (x, y), pt = heappop(paths)
        # print('--',steps, x, y)
        for i, j, m in [(1, 0, '>'), (-1, 0, '<'), (0, 1, 'v'), (0, -1, '^')]:
            if x + i >= 0 and x + i < w:
                if y + j >= 0 and y + j < h:
                    if (x + i, y + j) in visited:
                        continue
                    # check we can step
                    v0 = input[y][x]
                    v1 = input[y + j][x + i]
                    # print(v0, v1)
                    if ord(v1) - ord(v0) > 1:
                        continue
                    if (x + i, y + j) == end_pos:
                        return steps + 1
                    # print('ord', ord(v1) - ord(v0))
                    input2[y + j] = input2[y + j][:x + i] + m + input2[y + j][x + i + 1:]
                    visited.add((x + i, y + j))
                    heappush(paths, (steps + 1, (x + i, y + j), list(pt) + [v1]))  # (x+i, y+j, m)
    return 1_000_000

a_positions = []
p = 0
s = ''.join([''.join(row) for row in input])
while p != -1:
    p = s.find('a', p+1)
    if p >= 0:
        a_positions.append((p % w, p // w))

print('a_positions', a_positions)
print(len(a_positions))

l = []
for i, pos in enumerate(a_positions):
    if i%100==0:
        print(i)
    l.append(get_route(pos))

l.sort()
print(l)

