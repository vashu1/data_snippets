# Magic constants derived from the ALU code
As = [14, 13, 15, 13, -2, 10, 13, -15, 11, -9, -9, -7, -4, -6]
Bs = [0, 12, 14, 0, 3, 15, 11, 12, 1, 12, 3, 10, 14, 12]
Cs = [1, 1, 1, 1, 26, 1, 1, 26, 1, 26, 26, 26, 26, 26]
['div z 1', 'div z 1', 'div z 1', 'div z 1', 'div z 26', 'div z 1', 'div z 1', 'div z 26', 'div z 1', 'div z 26', 'div z 26', 'div z 26', 'div z 26', 'div z 26']

"""
4 ['div z 1', 'div z 1', 'div z 1', 'div z 1', 'div z 26', 'div z 1', 'div z 1', 'div z 26', 'div z 1', 'div z 26', 'div z 26', 'div z 26', 'div z 26', 'div z 26']
5 ['add x 14', 'add x 13', 'add x 15', 'add x 13', 'add x -2', 'add x 10', 'add x 13', 'add x -15', 'add x 11', 'add x -9', 'add x -9', 'add x -7', 'add x -4', 'add x -6']
15 ['add y 0', 'add y 12', 'add y 14', 'add y 0', 'add y 3', 'add y 15', 'add y 11', 'add y 12', 'add y 1', 'add y 12', 'add y 3', 'add y 10', 'add y 14', 'add y 12']
"""

# to get these, I split the input by "inp w" lines
# and diffed the blocks: the A is the varying x addend,
# the B the varying y addend and the C the varying z divisor
# (apparently always 1 or 26 depending on the sign of A)

"""
inp w
mul x 0
add x z
mod x 26
div z 1
add x 14
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 0
mul y x
add z y

inp w
x=z % 26
add x z
mod x 26
div z 1
add x 13
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
y=w+12
mul y x
add z y

"""

import itertools as it


# testing tools (not needed for the actual solution)

def forward(A, B, C, z, w):
    "this is what a single block does"
    z1 = z // C
    if w == z % 26 + A:
        return z1
    else:
        return 26 * z1 + w + B


def forward_all(ws, As=As, Bs=Bs, Cs=Cs, z=0):
    "the whole program"
    for A, B, C, w in zip(As, Bs, Cs, ws):
        z = forward(A, B, C, z, w)
    return z


# solution starts here

def backward(A, B, C, z2, w):
    """The possible values of z before a single block
    if the final value of z is z2 and w is w"""
    zs = []
    x = z2 - w - B
    if x % 26 == 0:
        zs.append(x // 26 * C)
    if 0 <= w - A < 26:
        z0 = z2 * C
        zs.append(w - A + z0)

    return zs


def solve(part, As=As, Bs=Bs, Cs=Cs):
    zs = {0}
    result = {}
    if part == 1:
        ws = range(1, 10)
    else:
        ws = range(9, 0, -1)
    for A, B, C in zip(As[::-1], Bs[::-1], Cs[::-1]):
        # print(len(zs))
        newzs = set()
        for w, z in it.product(ws, zs):
            z0s = backward(A, B, C, z, w)
            for z0 in z0s:
                newzs.add(z0)
                result[z0] = (w,) + result.get(z, ())
        zs = newzs
    return ''.join(str(digit) for digit in result[0])


print(solve(1))
print(solve(2))