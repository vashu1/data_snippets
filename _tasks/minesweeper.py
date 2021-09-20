import random
"""
TODO
rectangle board?
pack (mines, visible, flags) to GameState() ?

# lazy state
from collections import namedtuple, defaultdict
state = defaultdict(lambda: defaultdict(lambda: namedtuple('Cell', ['mine', 'visible', 'flag'], defaults=[random.random() < MINE_PROBABILITY, False, False])))
need to keep size separately, no bound control (
"""

MINE_PROBABILITY = 0.2
MAX_BOARD_SIZE = 10


def input_board_size():
    while True:
        txt = input('Board size? ')
        try:
            n = int(txt)
            if n < 1:
                print('Input positive number!')
            elif n > MAX_BOARD_SIZE:
                print(f'Sorry, max board size in {MAX_BOARD_SIZE}!')
            else:
                return n
        except:
            print('Input single number!')


def input_cell_coordinates(n):
    while True:
        txt = input('Input x, y (add "flag" to flag) ')
        flag = 'flag' in txt
        try:
            txt = [val for val in txt.strip().split(' ') if val and val != 'flag']
            if len(txt) != 2:
                print('Input 2 numbers!')
                continue
            x, y = txt
            x, y = int(x) - 1, int(y) - 1
            if not valid_coordinate(x, n):
                print(f'Input x in [1, {n}]')
                continue
            if not valid_coordinate(y, n):
                print(f'Input y in [1, {n}]')
                continue
            return x, y, flag
        except:
            print('Input 2 numbers!')


def valid_coordinate(v, n):
    return 0 <= v < n


def get_neigbours(cell_x, cell_y, n):
    square3x3 = [(x, y) for x in [cell_x-1, cell_x, cell_x+1] for y in [cell_y-1, cell_y, cell_y+1]]
    neigbours = [(x, y) for x, y in square3x3 if (x, y) != (cell_x, cell_y)]
    valid_neighbours = [(x, y) for x, y in neigbours if valid_coordinate(x, n) and valid_coordinate(y, n)]
    return valid_neighbours


def mine_count_in_neighbours(cell_x, cell_y, mines):
    return len([True for x, y in get_neigbours(cell_x, cell_y, len(mines)) if mines[y][x]])


def cell_character(x, y, mines, visible, flags):
    if flags[y][x]:
        return 'F'
    if not visible[y][x]:
        return '?'
    if mines[y][x]:
        return '*'
    count = mine_count_in_neighbours(x, y, mines)
    return '_' if count == 0 else str(count)


def show(mines, visible, flags):
    n = len(mines)
    for y in range(n):
        row_values = ''.join([cell_character(x, y, mines, visible, flags) for x in range(n)])
        print(row_values)


def play(mines, visible):
    n = len(mines)
    flags = [[False for _ in range(n)] for _ in range(n)]
    while True:
        show(mines, visible, flags)
        # check win
        cleared = lambda x, y: visible[y][x] or (flags[y][x] and mines[y][x])
        if all([cleared(x, y) for x in range(n) for y in range(n)]):
            print('YOU WON!')
            exit(0)
        # step
        x, y, flag = input_cell_coordinates(n)
        if flag:
            flags[y][x] = not flags[y][x]
            continue
        if flags[y][x]:
            print('Can\'t step on flag!')
            continue
        if mines[y][x]:
            print('YOUR DEAD!')
            exit(1)
        # clean
        cells_to_clean = [(x, y)]
        while cells_to_clean:
            x, y = cells_to_clean.pop()
            visible[y][x] = True
            if mine_count_in_neighbours(x, y, mines) == 0:
                for nx, ny in get_neigbours(x, y, n):
                    if not visible[ny][nx]:
                        cells_to_clean.append((nx, ny))



if __name__ == "__main__":
    n = input_board_size()
    mines = [[(random.random() < MINE_PROBABILITY) for _ in range(n)] for _ in range(n)]
    visible = [[False for _ in range(n)] for _ in range(n)]
    play(mines, visible)