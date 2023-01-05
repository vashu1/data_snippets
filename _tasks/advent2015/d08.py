test = '''""
"abc"
"aaa\\"aaa"
"\\x27"'''
def ln(line):
    res = 0
    indx = 0
    while indx < len(line):
        res += 1
        if line[indx] == '\\':
            if line[indx + 1] == '\\':
                indx += 1
            elif line[indx + 1] == '"':
                indx += 1
            elif line[indx + 1] == 'x':
                assert line[indx + 2] in '0123456789abcdef'
                assert line[indx + 3] in '0123456789abcdef'
                indx += 3
            else:
                assert False
        indx += 1
    return res

s1 = 0
s2 = 0
for line in open('d08.txt').readlines():  # test.split('\n'):
    line = line.strip()
    line = line[1:-1]
    s1 += len(line) + 2
    s2 += ln(line)

print(s1, s2, s1 - s2)

# part 2

def enc(line):
    res = []
    indx = 0
    while indx < len(line):
        res.append(line[indx])
        if line[indx] == '\\':
            res.append(line[indx])
            if line[indx + 1] == '\\':
                res.append(line[indx + 0])
                res.append(line[indx + 1])
                indx += 1
            elif line[indx + 1] == '"':
                res.append(line[indx + 0])
                res.append(line[indx + 1])
                indx += 1
            elif line[indx + 1] == 'x':
                assert line[indx + 2] in '0123456789abcdef'
                assert line[indx + 3] in '0123456789abcdef'
                res.append(line[indx + 1])
                res.append(line[indx + 2])
                res.append(line[indx + 3])
                indx += 3
            else:
                assert False
        indx += 1
    return ''.join(res)

s1 = 0
s2 = 0
for line in open('d08.txt').readlines():  # test.split('\n'):
    line = line.strip()
    line2 = enc(line[1:-1])
    #print(line, len(line2) + 6, len(line))
    s1 += len(line2) + 6
    s2 += len(line)

print(s1, s2, s1 - s2)
