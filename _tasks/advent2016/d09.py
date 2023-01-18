from collections import Counter, defaultdict
import os

test = 'X(8x2)(3x3)ABCY'
test = 'ADVENT'
test = 'A(1x5)BC'
test = '(3x3)XYZ'
test = '(6x1)(1x3)A'
test = 'X(8x2)(3x3)ABCY'
test = 'X(1x1)XX(1x1)AB'  # 8

res = defaultdict(Counter)

txt_name = __file__.split(os.sep)[-1].replace('.py', '.txt')
#for line in test.split('\n'):
for line in open(txt_name).readlines():
    line = line.strip()

ln = 0
indx = 0

while indx < len(line):
    s = line.find('(', indx)
    e = line.find(')', indx)
    #print(s, e)
    if s == -1:
        #print(ln, indx, len(line))
        ln += len(line) - indx
        break
    else:
        ln += s - indx
        marker = line[s+1:e]
        l, n = marker.split('x')
        l = int(l)
        n = int(n)
        #print(l, n, l*n)
        indx = e + l + 1
        ln += l * n

print(ln)

def llen(line):
    s = line.find('(')
    e = line.find(')')
    if s == -1:
        return len(line)
    marker = line[s + 1:e]
    l, n = marker.split('x')
    l = int(l)
    n = int(n)
    assert (e+1+l) <= len(line)
    return s + n * llen(line[e+1:e+1+l]) + llen(line[e+1+l:])

print(llen(line))
# high 137455