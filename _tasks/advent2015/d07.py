# https://ericpony.github.io/z3py-tutorial/guide-examples.htm
from z3 import *

BITS = 16

test = """123 -> x
456 -> y
x AND y -> d
x OR y -> e
x LSHIFT 2 -> f
y RSHIFT 2 -> g
NOT x -> h
NOT y -> i
8 RSHIFT 4 -> u"""
lines = test.split('\n')
lines = open('d07.txt').readlines()
lines = [l.strip() for l in lines]

values = {}
formulas = {}

variables = {}
data = {}
for line in lines:
    value, name = line.split(' -> ')
    variables[name] = BitVec(name, BITS)
    data[name] = value.split(' ')

for name in data:
    new_vals = []
    for val in data[name]:
        if val in set(['NOT', 'AND', 'OR', 'LSHIFT', 'RSHIFT']):
            new_vals.append(val)
        elif val.isnumeric():
            new_vals.append(BitVecVal(int(val), BITS))
        elif val in variables:
            new_vals.append(variables[val])
        else:
            assert False
    data[name] = new_vals

s = Solver()

# part 2
del data['b']
s.add(variables['b'] == BitVecVal(46065, BITS))

for name, values in data.items():
    if len(values) == 1:
        s.add(variables[name] == values[0])
    elif len(values) == 2 and values[0] == 'NOT':
        s.add(variables[name] == ~values[1])
    elif values[1] == 'AND' and len(values) == 3:
        s.add(variables[name] == values[0] & values[2])
    elif values[1] == 'OR' and len(values) == 3:
        s.add(variables[name] == values[0] | values[2])
    elif values[1] == 'LSHIFT' and len(values) == 3:
        s.add(variables[name] == values[0] << values[2])
    elif values[1] == 'RSHIFT' and len(values) == 3:
        s.add(variables[name] == LShR(values[0], values[2]))
    else:
        assert False, f'{name} = {values}'

# set_option(max_args=10000000, max_lines=1000000, max_depth=10000000, max_visited=1000000)

ch = s.check()
assert ch == sat

print(s.model().eval(variables['a']))
