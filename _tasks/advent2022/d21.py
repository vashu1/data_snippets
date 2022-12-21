from utils import *
import random

input_test = """root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32"""
input_test = input_test.split('\n')

input_full = open('d21.txt').readlines()

input = [l.strip() for l in input_full]


def isint(s):
    if isinstance(s, list):
        return False
    try:
        _ = int(s)
        return True
    except ValueError:
        return False


def solvable(line):
    a, _, b = line.split(' ')
    return isint(a) and isint(b)


# work out the number the monkey named root will yell

solved = {}
monkeys = {}


def resolve():
    for line in [line.strip() for line in input]:
        name, operation = line.split(':')
        operation = operation.strip()
        if isint(operation):
            solved[name] = int(operation)
        else:
            monkeys[name] = operation
    l = len(monkeys) + 1
    while l != len(monkeys):
        l = len(monkeys)
        for m in list(solved):
            for m2 in list(monkeys.keys()):
                if m in monkeys[m2]:
                    monkeys[m2] = monkeys[m2].replace(m, str(solved[m]))
                    if solvable(monkeys[m2]):
                        r = eval(monkeys[m2])
                        assert int(r) == r
                        solved[m2] = int(r)
                        del monkeys[m2]


resolve()
print('root', solved['root'])

# PART II

# monkey for the job starting with humn:. It isn't a monkey - it's you
# what number you need to yell so that root's equality check passes.

root = [line for line in input if line.startswith('root')][0]

input = [line for line in input if not line.startswith('root') and not line.startswith('humn')]

solved = {}
monkeys = {}
resolve()

def expr(r):
    if ' ' not in r:
        return r
    a, o, b = r.split(' ')
    if a in monkeys:
        a = expr(monkeys[a])
    if b in monkeys:
        b = expr(monkeys[b])
    if isint(b):
        b = int(b)
        if o == '-':
            o = '+'
            b = -b
    if isint(a):
        a = int(a)
        if o == '-':
           return [[b,'*',-1],'+',a]
        if o in ['+', '*']:
            return [b, o, a]
    return [a, o, b]

a, _, b = root.split(': ')[1].split(' ')
a = expr(monkeys[a])
b = int(solved[b])


def issim1(a):
    return isinstance(a, int) or isinstance(a, str)


def multiply(a, b):
    if isinstance(a, str):
        return [a,'*', b]
    aa, oo, bb = a
    if oo == '/':
        assert bb != 0
        return [multiply(aa, b), oo, bb]
    if oo == '*':
        return [aa, oo, bb*b]
    return [multiply(aa, b), oo, bb*b]


def simplify(v, level=0):
    if issim1(v):
        return v
    a, o, b = v
    if o == '*' and random.random() < 0.1:
        return multiply(a, b)
    if issim1(a):
        return v
    aa, oo, bb = a
    if o == '+' and oo == '+':
        #print('================ ++')
        return [aa, o, bb+b]
    if o == '*' and oo == '*':
        assert bb != 0 and b != 0
        #print('================ **')
        return [aa, o, bb*b]
    if level==0 and oo == '/' and o == '+' and bb != 0:
        return [aa,o,bb*b]
    return [simplify(a, level+1),o,b]

a = [a,'+',-b]

for _ in range(10_000):
    #print('\n')
    a = simplify(a)
    #print(a)

print(a)
print(int(- a[2] / a[0][2]))
