from utils import *

input_test = """30373
25512
65332
33549
35390"""
input_test = input_test.split('\n')

input_full = open('d08.txt').readlines()

input = [l.strip() for l in input_full]

rows = len(input)
cols = len(input[0])
visible = [([False] * cols) for _ in range(rows)]

def iterate_trees(coords):
    mx = -1
    for i, j in coords:
        val = int(input[i][j])
        if val > mx:
            visible[i][j] = True
            mx = val


for i in range(rows):
    iterate_trees([(i, j) for j in range(cols)])
    iterate_trees([(i, j) for j in range(cols-1, -1, -1)])

for j in range(cols):
    iterate_trees([(i, j) for i in range(rows)])
    iterate_trees([(i, j) for i in range(rows-1, -1, -1)])

print(len([v for v in flatten(visible) if v]))


def score2(height, coords):
    cnt = 0
    for i, j in coords:
        cnt += 1
        if int(input[i][j]) >= height:
            break
    return cnt


def score(coords):
    row, col = coords
    height = int(input[row][col])
    score = 1
    score *= score2(height, [(r, col) for r in range(row+1, rows)])
    score *= score2(height, [(r, col) for r in range(row - 1, -1, -1)])
    score *= score2(height, [(row, c) for c in range(col + 1, cols)])
    score *= score2(height, [(row, c) for c in range(col - 1, -1, -1)])
    return score

mx2 = -1
for i in range(rows):
    for j in range(cols):
        v = score((i, j))
        if v > mx2:
            mx2 = v

print(mx2)