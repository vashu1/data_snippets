value = '1'
value = '1113222113'


def parse(s):
    res = [[s[0]]]
    for c in s[1:]:
        if c != res[-1][-1]:
            res.append([c])
        else:
            res[-1].append(c)
    return [(len(i), int(i[-1])) for i in res]


def next_lsn(v):
    res = [str(count) + str(digit) for count, digit in parse(v)]
    return ''.join(res)


print(0, len(value))
for i in range(50):
    n = next_lsn(value)
    print(i + 1, len(n))
    value = n
