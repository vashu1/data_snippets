
test = '''NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C'''

input = '''KOKHCCHNKKFHBKVVHNPN

BN -> C
OS -> K
BK -> C
KO -> V
HF -> K
PS -> B
OK -> C
OC -> B
FH -> K
NV -> F
HO -> H
KK -> H
CV -> P
SC -> C
FK -> N
VV -> F
FN -> F
KP -> O
SB -> O
KF -> B
CH -> K
VF -> K
BH -> H
KV -> F
CO -> N
PK -> N
NH -> P
NN -> C
PP -> H
SH -> N
VO -> O
NC -> F
BC -> B
HC -> H
FS -> C
PN -> F
CK -> K
CN -> V
HS -> S
CB -> N
OF -> B
OV -> K
SK -> S
HP -> C
SN -> P
SP -> B
BP -> C
VP -> C
BS -> K
FV -> F
PH -> P
FF -> P
VK -> F
BV -> S
VB -> S
BF -> O
BB -> H
OB -> B
VS -> P
KB -> P
SF -> N
PF -> S
HH -> P
KN -> K
PC -> B
NB -> O
VC -> P
PV -> H
KH -> O
OP -> O
NF -> K
HN -> P
FC -> H
PO -> B
OH -> C
ON -> N
VN -> B
VH -> F
FO -> B
FP -> B
BO -> H
CC -> P
CS -> K
NO -> V
CF -> N
PB -> H
KS -> P
HK -> S
HB -> K
HV -> O
SV -> H
CP -> S
NP -> N
FB -> B
KC -> V
NS -> P
OO -> V
SO -> O
NK -> K
SS -> H'''

from collections import Counter

STEPS = 10
lines = input.split('\n')

def replace(sequence, rules):
    result = []
    for a, b in zip(sequence[:-1], sequence[1:]):
        result.append(a)
        if a+b in rules:
            result.append(rules[a+b])
    result.append(sequence[-1])
    return result

sequence = lines[0]
rules = {}
for line in lines[2:]:
    old, add = line.split(' -> ')
    assert old not in rules
    rules[old] = add

for i in range(STEPS):
    sequence = replace(list(sequence), rules)
    if i==0:
        print(''.join(sequence))
    print(i+1, len(sequence))

count = Counter(sequence)
print(count.most_common(1)[0])
print(count.most_common()[-1])

_, c1 = count.most_common(1)[0]
_, c2 = count.most_common()[-1]
print(c1 - c2)

# === phase 2

print('\n--- phase 2\n')

STEPS = 40
sequence = lines[0]

counts = Counter()
for a, b in zip(sequence[:-1], sequence[1:]):
    counts[a+b] += 1

print(sequence, counts)

def replace2(counts, rules):
    new_counts = Counter()
    for pair in counts:
        if pair in rules:
            a, b = pair
            c = rules[pair]
            new_counts[a + c] += counts[pair]
            new_counts[c + b] += counts[pair]
        else:
            new_counts[pair] += counts[pair]
    return new_counts

for i in range(STEPS):
    counts = replace2(counts, rules)
    if i == 0:
        print('===', counts)
    print(i + 1, sum(counts.values())+1)

count_letters = Counter()
for pair in counts:
    a, b = pair
    count_letters[a] += counts[pair]
    count_letters[b] += counts[pair]

print(count_letters.most_common(1)[0])
print(count_letters.most_common()[-1])
print(count_letters.most_common())

_, c1 = count_letters.most_common(1)[0]
_, c2 = count_letters.most_common()[-1]
c1 = int((c1+1)/2)
c2 = int((c2+1)/2)
print(c1 - c2)

"""
NCNBCHB
NC CN NB BC  CH HB
Counter({'NC': 1, 'CN': 1, 'NB': 1, 'BC': 1, 'CH': 1, 'HB': 1})

2192039569601.0
2192039569602

2188189693529
2188189693529
"""