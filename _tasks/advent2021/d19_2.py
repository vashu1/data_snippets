import numpy as np
import random
import itertools
from collections import defaultdict

THRESHOLD_DOTS_PER_SCANNER = 12
SIMILARITY_THRESHOLD = 50

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

def dot_ivariant_distance(dot1, dot2):
    return np.prod(np.abs(dot1 - dot2) + np.array([1,1,1]))  # add ones to stop single zero from spoiling invariant

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
scanner_beacons = defaultdict(list)
scanner_beacons[starting_scanner] = scanner_data[starting_scanner]
scanner_dot_invariants = defaultdict(set)
similar_dots = defaultdict(list)
for indx in scanner_data:
    for v in scanner_data[indx]:
        for j in scanner_data[indx]:
            if np.all(v == j):
                continue
            invariant = dot_ivariant_distance(v, j)
            similar_dots[invariant].append((indx, v, j))
            scanner_dot_invariants[indx].add(invariant)

similarity = {}
for i in scanner_dot_invariants:
    for j in scanner_dot_invariants:
        if i <= j:
            continue
        val = len(scanner_dot_invariants[i].intersection(scanner_dot_invariants[j]))
        similarity[(i, j)] = val
        similarity[(j, i)] = val

similar_dots2 = defaultdict(defaultdict(list))
for invariant in similar_dots:
    scanners = {scanner for scanner, _, _  in similar_dots[invariant]}
    for scanner in scanners:
        similar_dots2[scanner][invariant] += similar_dots[invariant]


cnt = 0
while len(transformations) != len(scanner_data):
    cnt += 1
    # pick scanner
    candidate_scanner = random.choice(list(scanner_data.keys()))
    if candidate_scanner in transformations:
        continue
    candidate_scanner2 = random.choice(list(transformations.keys()))
    similarity_value = similarity[(candidate_scanner, candidate_scanner2)]
    #print(similarity_value)
    if similarity_value < 50:  # THRESHOLD_DOTS_PER_SCANNER*(THRESHOLD_DOTS_PER_SCANNER-1)/2-10 ???
        continue
    #print(f'start {candidate_scanner=}')
    # pick dot
    candidate_dot_indx = random.randrange(len(scanner_data[candidate_scanner]))
    candidate_dot = scanner_data[candidate_scanner][candidate_dot_indx]
    # go through all transformations and count good dots
    for turn in transformation_combinations():
        for cur_beacon in scanner_beacons[candidate_scanner2]:
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
                print(f'{candidate_scanner=} {good_dot_count=} {bad_dot_found=} {cnt=} {similarity_value=} {len(transformations)=}')
            if (not bad_dot_found) and (good_dot_count >= THRESHOLD_DOTS_PER_SCANNER):
                transformations[candidate_scanner] = (turn, offset)
                for dot in scanner_data[candidate_scanner]:
                    true_dot = np.sum(dot * turn, axis=1) + offset
                    beacons[tuple(true_dot)] = true_dot
                    scanner_beacons[candidate_scanner].append(true_dot)
                break

print('task1', len(beacons))

max_dist = -1
for i in scanner_dot_invariants:
    for j in scanner_dot_invariants:
        if i <= j:
            continue
        _, position1 = transformations[i]
        _, position2 = transformations[j]
        dist = np.sum(np.abs(position1 - position2))
        if dist > max_dist:
            max_dist = dist

print('task2', max_dist)

# on test 2x faster  solves input in 2:30   1:27-1:50 after sorting similarity


