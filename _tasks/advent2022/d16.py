from utils import *
from collections import defaultdict, Counter, deque

input_test = """Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II"""
input_test = input_test.split('\n')

input_full = open('d16.txt').readlines()

input = [l.strip() for l in input_full]

# you have 30 minutes before the volcano erupts
# You estimate it will take you one minute to open a single valve and one minute to follow any tunnel from one valve to another.

# drop paths with 0s

caves = {}
useless = set()
for line in [line.strip() for line in input]:  # input_full input_test
    fst, snd = line.split('=')
    from_name = fst.split(' ')[1]
    rate, snd = snd.split(';')
    rate = int(rate)
    valves = snd.split('valve')[1][1:].strip().split(', ')
    assert from_name not in caves
    if rate == 0:
        useless.add(from_name)
    caves[from_name] = (rate, valves)


distances = defaultdict(lambda: defaultdict(lambda: 1_000_000))
for start in caves:
    distances[start][start] = 0
    stack = set([start])
    while stack:
        p = stack.pop()
        _, valves = caves[p]
        for valve in valves:
            assert p != valve  # no loops
            cur_d = distances[start][valve]
            impr = distances[start][p] + 1
            if impr < cur_d:
                distances[start][valve] = impr
                stack.add(valve)
    #print(start, distances[start])

# PART I

valves = set(caves.keys()) - useless
saved_valves = set(valves)
time = 0
path = []
stream = 0
best = 0

best_stream = None
best_path = None
all_paths = []

def run():
    global best, time, stream, best_stream, best_path, all_paths
    #print(f'{time=} {stream=} released={path[-1][0]} {best=} {path=} {valves=}')
    released, _, current = path[-1]
    if time > 30:
        all_paths.append(list(path))
        return
    if released + (30 - time) * stream > best:  # stay at place
        best = released + (30 - time) * stream
        best_stream = stream
        best_path = list(path)
        all_paths.append(list(path))
    for valve in list(valves):
        valves.remove(valve)
        dt = distances[current][valve] + 1
        time += dt
        released2 = released + stream * dt
        path.append((released2, dt - 1, valve))
        assert saved_valves - set([p[-1] for p in path]) == valves
        assert saved_valves - valves == set([p[-1] for p in path])
        stream += caves[valve][0]
        run()
        time -= distances[current][valve] + 1
        stream -= caves[valve][0]
        valves.add(valve)
        _ = path.pop()


for start in valves:
    path.append((0, distances['AA'][start], start))
    valves.remove(start)
    time = distances['AA'][start] + 1
    stream = caves[start][0]
    run()
    valves.add(start)
    _ = path.pop()


print(f'{best_stream=} {best_path=}')
print(best)


# PART II

max_release_all_valves = sum([caves[c][0] for c in caves])
valves = set(caves.keys()) - useless
path = [[], []]

best = 0
best_path = None
c = 0


def run():
    global best, time, stream, best_path, c
    c += 1
    if c % 1_000_000 == 0:
        print(c, best, path)
    ts = [p[-1][2] for p in path]
    min_t = min(ts)
    cur_best0 = sum([p[-1][0] for p in path]) + (26 - min_t) * max_release_all_valves
    if cur_best0 < best:  # does it stand a chance of beating best, drops 3/5 of paths
        return
    cur_best = 0
    for p in path:  # is it good already?
        released, stream, time, _ = p[-1]
        cur_best += released + (26 - time) * stream
        if cur_best > best:
            best = cur_best
            best_path = [list(p) for p in path]
    for i in range(len(path)):
        time = path[i][-1][-2]
        if time == min_t:
            for valve in list(valves):
                released, stream, time, current = path[i][-1]
                dt = distances[current][valve] + 1
                time += dt
                if time > 26:
                    continue
                valves.remove(valve)
                released2 = released + stream * dt
                stream += caves[valve][0]
                path[i].append((released2, stream, time, valve))
                run()
                _ = path[i].pop()
                valves.add(valve)


for start in list(valves):
    for start2 in list(valves):
        if start == start2:
            continue
        path[0] = [(0, caves[start][0], distances['AA'][start] + 1, start)]  # released stream time position
        valves.remove(start)
        path[1] = [(0, caves[start2][0], distances['AA'][start2] + 1, start2)]  # released stream time position
        valves.remove(start2)
        run()
        valves.add(start2)
        valves.add(start)


print(f'{best_path=}')
print(best)
