from collections import Counter
lines = open('input3.txt').readlines()

x = 0
y = 0
visits = Counter([(x, y)])
for v in lines[0]:
    if v == '<':
        x -= 1
    elif v == '>':
        x += 1
    elif v == '^':
        y += 1
    elif v == 'v':
        y -= 1
    else:
        assert False
    visits[(x, y)] += 1

print(len(visits))

def modify(state, idx, cmd):
    x, y = state[idx]
    if cmd == '<':
        x -= 1
    elif cmd == '>':
        x += 1
    elif cmd == '^':
        y += 1
    elif cmd == 'v':
        y -= 1
    else:
        assert False
    state[idx] = x, y

N = 2
state = [(0,0) for _ in range(N)]
visits = Counter(state)
for i, v in enumerate(lines[0]):
    idx = i%len(state)
    modify(state, idx, v)
    visits[state[idx]] += 1

print(len(visits))