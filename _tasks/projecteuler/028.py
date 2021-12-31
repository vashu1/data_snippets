# What is the sum of the numbers on the diagonals in a 1001 by 1001 spiral formed in the same way?

N = 1001

spiral = [1]
radius = 0

def step():
    global radius, spiral
    radius += 1
    spiral.append(spiral[-1] + 2*radius)
    spiral.append(spiral[-1] + 2*radius)
    spiral.append(spiral[-1] + 2*radius)
    spiral.append(spiral[-1] + 2*radius)

while radius < (N-1)//2:
    step()

print(sum(spiral))