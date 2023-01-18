from collections import Counter, defaultdict
import os

screen = [[0 for _ in range(50)] for _ in range(6)]


def print_screen():
    for y in range(len(screen)):
        print(''.join([('#' if v else '.') for v in screen[y]]))


test = '''rect 3x2
rotate column x=1 by 1
rotate row y=0 by 4
rotate column x=1 by 1'''

res = defaultdict(Counter)

txt_name = __file__.split(os.sep)[-1].replace('.py', '.txt')
#for line in test.split('\n'):
for line in open(txt_name).readlines():
    line = line.strip()
    if line.startswith('rect '):
        x, y = line.split(' ')[1].split('x')
        x = int(x)
        y = int(y)
        for xx in range(x):
            for yy in range(y):
                screen[yy][xx] = 1
    elif line.startswith('rotate row y='):
        a, b = line.split('=')[1].split(' by ')
        a = int(a)
        b = int(b)
        cp = [v for v in screen[a]]
        for i, c in enumerate(cp):
            screen[a][(i + b) % len(screen[0])] = c
    elif line.startswith('rotate column x='):
        a, b = line.split('=')[1].split(' by ')
        a = int(a)
        b = int(b)
        cp = [screen[i][a] for i in range(len(screen))]
        for i, c in enumerate(cp):
            screen[(i + b) % len(screen)][a] = c
    else:
        print(line)
        assert False
    print(line)
    print_screen()




print('\n\n', sum([sum(lst) for lst in screen]))

'''rect AxB
rotate row y=A by B
rotate column x=A by B'''