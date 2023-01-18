from collections import Counter, defaultdict
import os

test = '''eedadn
drvtee
eandsr
raavrd
atevrs
tsrnev
sdttsa
rasrtv
nssdts
ntnada
svetve
tesnvt
vntsnd
vrdear
dvrsen
enarar'''

res = defaultdict(Counter)

txt_name = __file__.split(os.sep)[-1].replace('.py', '.txt')
#for line in test.split('\n'):
for line in open(txt_name).readlines():
    line = line.strip()
    for i, c in enumerate(line):
        res[i][c] += 1

print(''.join([res[c].most_common()[0][0] for c in res]))
print(''.join([res[c].most_common()[-1][0] for c in res]))