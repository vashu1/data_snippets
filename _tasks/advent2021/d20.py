
test = '''..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..##
#..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###
.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#.
.#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#.....
.#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#..
...####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.....
..##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###'''

BORDER = 60

# light pixels (#) and dark pixels (.)    1 and 0
# infinite    input image; the rest of the input image consists of dark pixels (.)
# simultaneously

# apply twice, count lit

algo = []
image0 = []
processing_image = False
#lines = test.split('\n')
lines = [i.strip() for i in open('input20.txt').readlines()]

for line in lines:
    if not line:
        processing_image = True
        continue
    if processing_image:
        image0.append(list(line))
    else:
        algo.append(line)


algo = ''.join(algo)
assert len(algo) == 512
#assert algo[0] == '.'

h, w = len(image0), len(image0[0])
h2 = 2*BORDER + h
w2 = 2*BORDER + w
image = []
for i in range(BORDER):
    image.append(['.'] * w2)

for i in image0:
    image.append(['.'] * BORDER + i + ['.'] * BORDER)

for i in range(BORDER):
    image.append(['.'] * w2)


def get_index(image, x, y):
    res = image[y-1][x-1:x+2] + image[y][x-1:x+2] + image[y+1][x-1:x+2]
    res = ''.join(res)
    res = res.replace('#', '1').replace('.', '0')
    return int(res, 2)


def print_image(image):
    for row in image:
        print(''.join(row)[:200])
    print('\n')

def run_step(image, i):
    new_image = []
    filler = '#' if i%2==0 else '.'
    new_image.append([filler] * w2)
    for y in range(1, h2-1):
        row = [filler]
        for x in range(1, w2-1):
            i = get_index(image, x, y)
            row.append(algo[i])
        row.append(filler)
        new_image.append(row)
    new_image.append([filler] * w2)
    return new_image

for i in range(2):
    image = run_step(image, i)
    # print_image(image)

print('task1', sum([row.count('#') for row in image]))

for i in range(48):
    image = run_step(image, i)

#print_image(image)
print('task2', sum([row.count('#') for row in image]))