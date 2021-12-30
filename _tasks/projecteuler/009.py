# one Pythagorean triplet for which a + b + c = 1000.

N = 1000
squares = {n:n**2 for n in range(1, N)}
for a in range(1, N):
    for b in range(a, N):
        c = N - a - b
        if c < 1:
            continue
        if squares[a] + squares[b] == squares[c]:
            print(f'{a=} {b=} {c=} {a+b+c=} {a*b*c=}')