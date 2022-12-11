"""

"""
from utils import *
from collections import defaultdict, Counter, deque

input_test = """addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop"""
input_test = input_test.split('\n')

input_full = open('d10.txt').readlines()

x = 1
x_vals = [x]
tact = 0
for line in input_full:
    line = line.strip()
    if line == 'noop':
        x_vals.append(x)
    elif line.startswith('addx '):
        x_vals.append(x)
        x_vals.append(x)
        _, v = line.split(' ')
        v = int(v)
        x += v
    else:
        print(line)
        assert False

# Find the signal strength during the 20th, 60th, 100th, 140th, 180th, and 220th cycles. What is the sum of these six signal strengths?
print(len(x_vals)-1)
print(sum([indx * x_vals[indx] for indx in range(20, 220+1, 40)]))

# the sprite is 3 pixels wide, and the X register sets the horizontal position of the middle of that sprite
# pixels on the CRT: 40 wide and 6 high
# The left-most pixel in each row is in position 0, and the right-most pixel in each row is in position 39

crt = [['.']*40 for _ in range(6)]
for i in range(0, 240):
    if abs(x_vals[i+1] - (i%40)) <= 1:
        crt[i//40][i%40] = '#'

for j in range(6):
    print(''.join(crt[j]))