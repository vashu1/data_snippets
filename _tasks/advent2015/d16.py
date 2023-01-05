test = {
    'children': 3,
    'cats': 7,
    'samoyeds': 2,
    'pomeranians': 3,
    'akitas': 0,
    'vizslas': 0,
    'goldfish': 5,
    'trees': 3,
    'cars': 2,
    'perfumes': 1,
}

for line in open('d16.txt').readlines():  # ['Sue 161: vizslas: 5, akitas: 0, samoyeds: 2']:#
    line = line.strip()
    # Sue 16: vizslas: 6, cats: 6, pomeranians: 10
    i = line.index(':')
    s = line[:i]
    vals = line[i+1:]
    data = {}
    for val in vals.split(', '):
        k, v = val.split(': ')
        k = k.strip()
        v = int(v)
        data[k] = v
    bad = False
    for i in test:
        if i in data:
            # part 1
            #if test[i] != data[i]:
            #    bad = True
            # part 2
            if i in ['cats', 'trees']:
                if test[i] >= data[i]:
                    bad = True
            elif i in ['pomeranians', 'goldfish']:
                if test[i] <= data[i]:
                    bad = True
            else:
                if test[i] != data[i]:
                    bad = True
    if bad:
        continue
    print(s, data)

