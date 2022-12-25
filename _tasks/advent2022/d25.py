MAX_DIGITS = 50

input_test = """1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122"""
input_test = input_test.split('\n')

input_full = open('d25.txt').readlines()

input = [l.strip() for l in input_full]  # input_full input_test


def decode_single(i):
    return {
        '=': -2,
        '-': -1,
        '0': 0,
        '1': 1,
        '2': 2,
    }[i]


def encode_single(i):
    return {
        -2: '=',
        -1: '-',
        0: '0',
        1: '1',
        2: '2',
    }[i]


def decode(line):
    v = 1
    res = 0
    for i in reversed(line):
        res += v * decode_single(i)
        v *= 5
    return res


# max number we can encode with n+1 digits
max_c = {0: 2}
for i in range(1, MAX_DIGITS):
    l = 5 ** i
    max_c[i] = 3 * l + max_c[i - 1]


def encode(v, digits):
    if abs(v) > max_c[digits]:
        return None
    if digits == 0:
        return [v]
    for j in [-2, -1, 0, 1, 2]:
        cur = j * (5 **  digits)
        r = encode(v - cur, digits - 1)
        if r:
            r.append(j)
            return r
    return None


# sum input
s = 0
for line in [line.strip() for line in input]:
    v = decode(line)
    #print(line, v)
    s += v

print(s)

# encode output
q = None
d = 0
while not q:
    q = encode(s, digits=d)
    #print('d', d, 'res', q)
    d += 1

# int array to string
s = '' .join([encode_single(v) for v in reversed(q)])
print(s)
