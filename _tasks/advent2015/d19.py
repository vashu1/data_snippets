from collections import defaultdict, Counter
import parse
import os


def split_formula(formula):
    res = []
    i = 0
    while i < len(formula):
        if i + 1 < len(formula) and formula[i + 1].islower():
            res.append(formula[i:i+2])
            i += 2
        else:
            res.append(formula[i])
            i += 1
    return res


test = """H => HO
H => OH
O => HH

HOHOHO"""

txt_name = __file__.split(os.sep)[-1].replace('.py', '.txt')
lines = test.split('\n')
lines = open(txt_name).readlines()
lines = [l.strip() for l in lines]

start = lines[-1]
reactions = defaultdict(list)

lines = lines[:-2]
for line in lines:
    s, r = line.split(' => ')
    reactions[s].append(split_formula(r))


def all_results(formula):
    formula = split_formula(formula)
    res = set()
    for s in reactions:
        for index, v in enumerate(formula):
            if v == s:
                for sub in reactions[s]:
                    lst = list(formula[:index]) + sub + list(formula[index+1:])
                    res.add(''.join(lst))
    return res

r = all_results(start)
print(r)
print(len(r))

# part 2

pairs = set()
lns = {}
for s in reactions:
    for r in reactions[s]:
        t = (s, ''.join(r))
        pairs.add(t)
        lns[t] = 1

for k in range(6):
    print('ITERATION', k, len(pairs))
    pairs2 = set()
    for r, s in pairs:
        t0 = (r, s)
        pairs2.add(t0)
        for ss in all_results(s):
            t = (r, ss)
            if t not in lns:
                pairs2.add(t)
                lns[t] = lns[t0] + 1
    pairs = pairs2

print('ITERATIONs', len(pairs), max([len(s) for r, s in pairs]))

pairs = list(pairs)
pairs.sort(key=lambda x: -len(x[1]))

print(len(start))
c = 0
cc = []
def shortened(formula, steps):
    for s, r in pairs:
        i = 0
        while r in formula[i:]:
            global c, cc
            c += 1
            if c % 1000000==0:
                print(c, len(formula), steps, formula)
            i = formula.index(r)
            formula2 = formula[:i] + s + formula[i+len(r):]
            #assert len(formula2) < len(formula), f'{r=} {s=}'
            if formula2 == 'e':
                print(steps, s, r, lns[(s, r)])
                cc.append(lns[(s, r)])
                return True
            if steps > 0:
                rr = shortened(formula2, steps + lns[(s, r)])
                if rr:
                    print(steps, s, r, lns[(s, r)])
                    cc.append(lns[(s, r)])
                    return True
            i += 1
    return False

steps = 1
r = shortened(start, steps)
print('--', steps, r, cc, sum(cc))

