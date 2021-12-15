# https://adventofcode.com/2021/day/9

test = """2199943210
3987894921
9856789892
8767896789
9899965678"""
vals = test.split('\n')
# comment out next line to run test
vals = [line.strip() for line in open('input').readlines()]

n = len(vals[0])
vals = [f'9{val}9' for val in vals]
vals = ['9'*(n+2)]+vals+['9'*(n+2)]
vals = [list(map(int, list(line))) for line in vals]

count = 0
score = 0
lowest = []
for y in range(1, len(vals)-1):
  for x in range(1, len(vals[0])-1):
    l, r, u, d = vals[y][x-1], vals[y][x+1], vals[y+1][x], vals[y-1][x]
    if vals[y][x] < min(l, r, u, d):
      count += 1
      score += 1 + int(vals[y][x])
      lowest.append((x,y))

print(count, score)

# === part 2

def fill_flat(dots, new_val):
  next_new_val = 9
  new_dots = []
  for x,y in dots:
    for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
      new_dot = (x+dx, y+dy)  #TODO need to iterate only border to avoid n^2
      if new_dot not in dots:
        if vals[y+dy][x+dx] == new_val:
          new_dots.append(new_dot)
        else:
          next_new_val = min(next_new_val, vals[y+dy][x+dx])
  dots.update(new_dots)
  indx = 0
  while indx < len(new_dots):
    x,y = new_dots[indx]
    for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
      new_dot = (x+dx, y+dy)
      if new_dot not in dots:
        if vals[y+dy][x+dx] < new_val:
          return -1, set()
        elif vals[y+dy][x+dx] == new_val:
          dots.add(new_dot)
          new_dots.append(new_dot)
        else:
          next_new_val = min(next_new_val, vals[y+dy][x+dx])
    indx += 1
  return next_new_val, dots

def get_basin_size(x, y):
  flat_part = set([(x,y)])
  l, r, u, d = vals[y][x-1], vals[y][x+1], vals[y+1][x], vals[y-1][x]
  next_new_val = min(l, r, u, d)
  while True:
    prev_result = len(flat_part)
    next_new_val, flat_part = fill_flat(flat_part, next_new_val)
    if next_new_val == -1:
      return prev_result
    if next_new_val == 9:
      return len(flat_part)
  return result

sizes = []
for x,y in lowest:
  sizes.append(get_basin_size(x, y))

sizes.sort()
print(sizes[-1]*sizes[-2]*sizes[-3])


# improved

from collections import defaultdict
def fill(x,y):
    cells = defaultdict(set)
    result = lambda cells, level: sum([len(cells[i]) for i in range(0, level - 1)])
    level = vals[y][x]
    cells[level].add((x,y))
    queue = [(x, y)]
    index = 0
    while True:
        x, y = queue[index]
        for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
            x2,y2 = x+dx, y+dy
            v2 = vals[y2][x2]
            if (x2, y2) in cells[v2] or v2 == 9:
                continue
            if v2 < level:
                return result(cells, level)
            cells[v2].add((x2, y2))
            queue.append((x2, y2))
        index += 1
        if index >= len(queue):  # level-up
            while True:
                level += 1
                if level == 9:  # if we had tons of levels we would keep track of next level with heap
                    return result(cells, level+1)
                if level in cells:
                    break
            index = 0
            queue = list(cells[level])

sizes = []
for x,y in lowest:
  sizes.append(fill(x,y))

sizes.sort()
print(sizes[-1]*sizes[-2]*sizes[-3])