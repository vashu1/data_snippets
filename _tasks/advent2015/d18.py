from collections import defaultdict, Counter
import parse
import os

SZ = 100
STEPS_1 = 100


def flatten(lst):
    return [item for sublist in lst for item in sublist]


def new_board():
    return [[0] * SZ for _ in range(SZ)]


def count_neighbours(board, x, y):
    cnt = 0
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            nx = x + dx
            ny = y + dy
            if 0 <= nx < SZ:
                if 0 <= ny < SZ:
                    if board[ny][nx]:
                        cnt += 1
    return cnt


def corners_on(board):
    board[0][0] = 1
    board[SZ - 1][0] = 1
    board[0][SZ - 1] = 1
    board[SZ - 1][SZ - 1] = 1


board = new_board()

y = 0
txt_name = __file__.split(os.sep)[-1].replace('.py', '.txt')
for line in open(txt_name).readlines():
    line = line.strip()
    for x, ch in enumerate(line):
        board[y][x] = 1 if ch == '#' else 0
    y += 1

corners_on(board)

for i in range(STEPS_1):
    board2 = new_board()
    for x in range(SZ):
        for y in range(SZ):
            cnt = count_neighbours(board, x, y)
            if board[y][x]:
                if cnt in [2, 3]:
                    board2[y][x] = 1
            else:
                if cnt == 3:
                    board2[y][x] = 1
    board = board2
    corners_on(board)
    print(i+1, sum(flatten(board)))


#print(sum(flatten(board)))

# part 2
