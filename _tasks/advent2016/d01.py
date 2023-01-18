
data = '''R4, R1, L2, R1, L1, L1, R1, L5, R1, R5, L2, R3, L3, L4, R4, R4, R3, L5, L1, R5, R3, L4, R1, R5, L1, R3, L2, R3, R1, L4, L1, R1, L1, L5, R1, L2, R2, L3, L5, R1, R5, L1, R188, L3, R2, R52, R5, L3, R79, L1, R5, R186, R2, R1, L3, L5, L2, R2, R4, R5, R5, L5, L4, R5, R3, L4, R4, L4, L4, R5, L4, L3, L1, L4, R1, R2, L5, R3, L4, R3, L3, L5, R1, R1, L3, R2, R1, R2, R2, L4, R5, R1, R3, R2, L2, L2, L1, R2, L1, L3, R5, R1, R4, R5, R2, R2, R4, R4, R1, L3, R4, L2, R2, R1, R3, L5, R5, R2, R5, L1, R2, R4, L1, R5, L3, L3, R1, L4, R2, L2, R1, L1, R4, R3, L2, L3, R3, L2, R1, L4, R5, L1, R5, L2, L1, L5, L2, L5, L2, L4, L2, R3'''
#data = 'R5, L5, R5, R3'
#data = 'R2, L3'
#data = 'R8, R4, R4, R8'

x, y = 0, 0
heading = 0, 1
visited = set([(x, y)])

def turn_left():
    global heading
    xx, yy = heading
    xx_ = xx * 0 - yy * 1
    yy_ = xx * 1 + yy * 0
    heading = xx_, yy_

for cmd in data.split(', '):
    direction = cmd[0]
    steps = int(cmd[1:])
    if direction == 'L':
        turn_left()
    elif direction == 'R':
        turn_left()
        turn_left()
        turn_left()
    else:
        assert False
    for _ in range(steps):
        x += heading[0]
        y += heading[1]
        if (x, y) in visited:
            print(x, y)
            print(abs(x) + abs(y))
            exit(1)
        visited.add((x, y))

print(x, y)
print(abs(x) + abs(y))