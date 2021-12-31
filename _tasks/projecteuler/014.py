# Longest Collatz sequence
# Which starting number, under one million, produces the longest chain?

def collatz_generator(n):
    yield n
    while n > 1:
        if n % 2 == 0:  # even
            n //= 2
        else:
            n = 3 * n + 1
        yield n

assert list(collatz_generator(13)) == [13, 40, 20, 10, 5, 16, 8, 4, 2, 1]

used_numbers = set()

max_n = None
max_len = 0
for n in range(1_000_000-1, 0, -1):
    if n % 10_000 == 0:
        print(f'progress {n}')
    if n in used_numbers:  # improves performance  25s -> 9s
        continue
    cur_seq = list(collatz_generator(n))
    cur_len = len(cur_seq)
    used_numbers.update(cur_seq)
    if cur_len > max_len:
        max_len = cur_len
        max_n = n

print(f'{max_len=} {max_n=}')