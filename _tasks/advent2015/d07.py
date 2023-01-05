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
NOT y -> i"""
lines = test.split('\n')
#lines = open('d07.txt').readlines()
lines = [l.strip() for l in lines]

values = {}
formulas = {}

variables = {}
data = {}
for line in lines:
    value, name = line.split(' -> ')
    variables[name] = BitVec(name, BITS)
    data[name] = value.split(' ')

s = Solver()

for name, values in data.items():
    if len(values) == 1:
        if values[0].isnumeric():
            s.add(variables[name] == int(value))
        else:
            s.add(variables[name] == variables[values[0]])
    elif values[0] == 'NOT':
        s.add(variables[name] == ~variables[values[1]])
    elif values[1] == 'AND':
        s.add(variables[name] == variables[values[0]] & variables[values[2]])
    elif values[1] == 'OR':
        s.add(variables[name] == variables[values[0]] | variables[values[2]])
    elif values[1] == 'LSHIFT':
        s.add(variables[name] == LShR(variables[values[0]], variables[values[2]]))
    elif values[1] == 'RSHIFT':
        s.add(variables[name] == RShR(variables[values[0]], variables[values[2]]))
    else:
        assert False

for name in sorted(variables.keys()):
    print(name, s(variables[s]))

#print(s(variables['a']))