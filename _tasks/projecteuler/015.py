import numpy as np

# Starting in the top left corner of a 2×2 grid, and only being able to move to the right and down, there are exactly 6 routes to the bottom right corner.
# How many such routes are there through a 20×20 grid?

def routes(x, y):
    result = [[1]*(x+1)]  # 1xX lattice
    while len(result) <= y:
        row = [1]
        for i in range(1,x+1):
            row.append(row[-1]+result[-1][i])
        result.append(row)
    return result[-1][-1]

print(f'{routes(20, 20)=}')

