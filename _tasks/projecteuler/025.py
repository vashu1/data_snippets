from collections import Counter
fib = [1, 1]

N = 1_000

while len(str(fib[-1])) < N:
    fib.append(fib[-1] + fib[-2])

print(len(fib))