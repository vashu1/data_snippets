import numpy as np
import random
import itertools
from collections import defaultdict

THRESHOLD_DOTS_PER_SCANNER = 12

random.seed(1)

ooo = np.array([0, 0, 0])
ox = np.array([1, 0, 0])
oy = np.array([0, 1, 0])
oz = np.array([0, 0, 1])
all_directions = [+ox, +oy, +oz, -ox, -oy, -oz]

lines = [line.strip() for line in open('input19.txt').readlines()]
current_scanner = -1
scanner_data = defaultdict(list)
for line in lines:
    if line.startswith('---'):  # e.g. '--- scanner 0 ---'
        current_scanner = int(line.split(' ')[2])
        continue
    if not line:
        continue
    vals = line.split(',')
    assert len(vals) == 3
    scanner_data[current_scanner].append(np.array(list(map(int, vals))))


def transformation_combinations():
    for i in all_directions:
        for j in all_directions:
            if np.all(j == i) or np.all(j == -i):
                continue
            yield [i, j, np.cross(i,j)]


def dot_in_range(scanner_position, dot):
    res = np.abs(scanner_position - dot)
    res = np.max(res)
    return res <= 1000


transformations = {}
starting_scanner = random.choice(list(scanner_data.keys()))
transformations[starting_scanner] = (np.array([ox, oy, oz]), ooo)
beacons = {tuple(v):v for v in scanner_data[starting_scanner]}

while len(transformations) != len(scanner_data):
    # pick scanner
    candidate_scanner = random.choice(list(scanner_data.keys()))
    if candidate_scanner in transformations:
        continue
    print(f'start {candidate_scanner=}')
    # pick dot
    candidate_dot_indx = random.randrange(len(scanner_data[candidate_scanner]))
    candidate_dot = scanner_data[candidate_scanner][candidate_dot_indx]
    # go through all transformations and count good dots
    for turn in transformation_combinations():
        for cur_beacon in beacons.values():
            candidate_dot_turned = np.sum(candidate_dot*turn, axis=1)
            offset = cur_beacon - candidate_dot_turned
            good_dot_count = 0
            bad_dot_found = 0
            bads=[]
            for dot in scanner_data[candidate_scanner]:
                true_dot = np.sum(dot*turn, axis=1) + offset
                if tuple(true_dot) in beacons:
                    good_dot_count += 1
                else:  # dot is not located
                    for scanner in transformations:
                        _, position = transformations[scanner]
                        if dot_in_range(position, true_dot):  # if dot is in range - then it is bad
                            bad_dot_found += 1
                            bads.append(true_dot)
                            break
            if good_dot_count>1:
                print(f'{candidate_scanner=} {good_dot_count=} {bad_dot_found=} {len(transformations)=}')
            if (not bad_dot_found) and (good_dot_count >= THRESHOLD_DOTS_PER_SCANNER):
                transformations[candidate_scanner] = (turn, offset)
                for dot in scanner_data[candidate_scanner]:
                    true_dot = np.sum(dot * turn, axis=1) + offset
                    beacons[tuple(true_dot)] = true_dot
                break

print(len(beacons))

# 33m35.503s to get 12scanners out of 36