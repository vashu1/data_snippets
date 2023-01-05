from collections import defaultdict
import parse

VERY_BIG = int(1e9)
VERY_SMALL = -1

test = """London to Dublin = 464
London to Belfast = 518
Dublin to Belfast = 141"""

graph = defaultdict(dict)
points = set()

#for line in test.split('\n'):
for line in open('d09.txt').readlines():
    line = line.strip()
    p1, p2, ln = parse.parse('{} to {} = {:d}', line)
    graph[p1][p2] = ln
    graph[p2][p1] = ln
    points.add(p1)
    points.add(p2)


def best_for_start(start, visited, best, start_val, f):
    visited.add(start)
    if visited == points:
        visited.remove(start)
        return 0
    res = start_val
    for next in graph[start]:
        if next in visited:
            continue
        s = graph[start][next]
        v = best_for_start(next, visited, best - s, start_val, f)
        res = f(res, s + v)
    visited.remove(start)
    return res


def best_all(f, start_val):
    res = start_val
    for start in points:
        v = best_for_start(start, set(), res, start_val, f)
        res = f(res, v)
    return res


res = best_all(min, VERY_BIG)  # shortest
print(res)

res = best_all(max, VERY_SMALL)  # longest
print(res)