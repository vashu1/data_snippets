# optimise gcode for laser engraver
# - revert rows and drop low intensity pixels
INPUT_FNAME = 'australia4.gcode'
OUTPUT_FNAME = 'australia5.gcode'

OPENING_LINES_COUNT = 4
ENDING_LINES_COUNT  = 4
STEP_LINES_COUNT    = 4

def print_block(name, block):
    print name
    for i in block:
        print '\t' + i
    print ''

def validate_step(step):
    res = len(step) == STEP_LINES_COUNT
    res &= step[0].startswith('G0 Y')
    res &= step[1] == 'M106'
    res &= step[2].startswith('G4 P')
    res &= step[3] == 'M107 P1'
    return res

def flatten(l):
    return [item for sublist in l for item in sublist]

def get_step_x(step):
    return float(step[0].split(' ')[2][1:])

def get_step_y(step):
    return float(step[0].split(' ')[1][1:])

def get_step_t(step):
    return float(step[2].split(' ')[1][1:])

lines = [x.strip() for x in open(INPUT_FNAME).readlines()]

opening = lines[:OPENING_LINES_COUNT]
ending = lines[-ENDING_LINES_COUNT:]
print_block('OPENING:', opening)
print_block('ENDING:', ending)

body = [[]]
for i in lines[OPENING_LINES_COUNT:-ENDING_LINES_COUNT]:
    if len(body[-1]) == STEP_LINES_COUNT:
        if not validate_step(body[-1]):
            print_block('Bad step:', body[-1])
        body.append([])
    body[-1].append(i)

# stats
from collections import Counter
c = Counter()
for s in body:
    c[get_step_t(s)] += 1

print c
# print len(filter(lambda s: get_step_t(s) > 29, body))

# drop steps with low time
body = filter(lambda s: get_step_t(s) > 5, body)

body_lines = [[]]
y = get_step_y(body[0])
for step in body:
    if y != get_step_y(step):
        body_lines.append([])
        y = get_step_y(step)
    body_lines[-1].append(step)

# reverse odd strings
for i in range(len(body_lines)):
    body_lines[i].sort(key = get_step_x, reverse = (i % 2 == 1)) #.reverse()

body = flatten(body)

# save data
f = open(OUTPUT_FNAME, 'w+')
f.writelines([(x + '\n') for x in opening])
f.writelines([(x + '\n') for x in body])
f.writelines([(x + '\n') for x in ending])
f.close()