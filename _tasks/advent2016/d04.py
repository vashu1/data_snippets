import os
from collections import Counter

test = '''aaaaa-bbb-z-y-x-123[abxyz]
a-b-c-d-e-f-g-h-987[abcde]
not-a-real-room-404[oarel]
totally-real-room-200[decoy]'''  # 1110


def chksum(s):
    s = s.replace('-', '')
    mc = Counter(s).most_common()
    mc.sort(key=lambda v: -v[1]*10_000 + ord(v[0]))
    return ''.join([c for c, _ in mc])[:5]

def decode_char(c, s):
    if c == '-':
        return ' '
    val = (ord(c) - ord('a') + s) % 26
    return chr(ord('a') + val)


def decode(s, sec):
    return ''.join([decode_char(c, sec) for c in s])


assert decode('qzmt-zixmtkozy-ivhz', 343) == 'very encrypted name'

sector_sum = 0
coded = []

txt_name = __file__.split(os.sep)[-1].replace('.py', '.txt')
#for line in test.split('\n'):
for line in open(txt_name).readlines():
    line = line.strip()
    assert line[-1] == ']'
    a, chk = line[:-1].split('[')
    vals = a.split('-')
    name = '-'.join(vals[:-1])
    sector = int(vals[-1])
    coded.append((name, sector))
    #print(chksum(name), chk)
    if chksum(name) == chk:
        #print(line)
        sector_sum += sector

print(sector_sum)

for nm, sc in coded:
    s = decode(nm, sc)
    if 'pole' in s:
        print(nm, s, sc)