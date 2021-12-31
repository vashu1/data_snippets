input = '0123456789'


def next_perm(perm):  # wrote version of this in assembler years ago, lol
    assert isinstance(perm, list)
    for i in range(len(perm)-2, 0-1, -1):
        a, b = perm[i:i+2]
        if a < b:
            min_next_index = i+1
            for j in range(i+2, len(perm)):
                if perm[j] > a and perm[j] < perm[min_next_index]:
                    min_next_index = j
            perm[i], perm[min_next_index] = perm[min_next_index], perm[i]
            perm[i+1:len(perm)] = sorted(perm[i+1:len(perm)])
            return

if __name__ == '__main__':
    perm = list(input)
    c = 1
    while c < 1_000_000:
        c += 1
        next_perm(perm)
    print(''.join(perm))
