
test = '''5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526'''

input = '''4781623888
1784156114
3265645122
4371551414
3377154886
7882314455
6421348681
7175424287
5488242184
2448568261'''

data = [list(map(int, line)) for line in input.split('\n')]

# An octopus can only flash at most once per step.)
# How many total flashes are there after 100 steps?

def neighbours(x,y):
    for dx in range(-1,1+1):
        for dy in range(-1, 1 + 1):
            if dx == 0 and dy == 0:
                continue
            if x+dx < 0 or y+dy < 0:
                continue
            if x+dx >= len(data[0]) or y+dy >= len(data):
                continue
            yield x+dx, y+dy


def run_step():
    extra = set()
    for y in range(len(data)):
        for x in range(len(data[0])):
            data[y][x] += 1
            if data[y][x] > 9:
                data[y][x] = 0
                extra.add((x,y))
    blinks = set()
    extra2 = set()
    while True:
        for x,y in extra:
            for x2,y2 in neighbours(x,y):
                if (x2,y2) not in blinks and (x2,y2) not in extra and (x2,y2) not in extra2:
                    data[y2][x2] += 1
                    if data[y2][x2] > 9:
                        data[y2][x2] = 0
                        extra2.add((x2, y2))
        blinks.update(extra)
        extra = extra2
        extra2 = set()
        if not extra:
            return len(blinks)

def run_step2():  # more efficient, cleaner code
    result = 0
    blink = []
    for y in range(len(data)):  # initial increment
        for x in range(len(data[0])):
            data[y][x] += 1
            if data[y][x] > 9:
                result += 1
                blink.append((x,y))
    while True:
        if not blink:  # drop blinked to zero and return
            for y in range(len(data)):
                for x in range(len(data[0])):
                    if data[y][x] > 9:
                        data[y][x] = 0
            return result
        x, y = blink.pop()
        for x2, y2 in neighbours(x, y):  # chain reaction
            data[y2][x2] += 1
            if data[y2][x2] == 10:  # ==10, cause we want to process blink only once
                result += 1
                blink.append((x2, y2))

# step 11

#print(sum([run_step2() for i in range(100)]))
#exit(0)

# step 2

n = 1
while run_step2() != len(data)*len(data[0]):
    n +=1

print(n)