
test1 = '''start-A
start-b
A-c
A-b
b-d
A-end
b-end'''

test2 = '''dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc'''

test3 = '''fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW'''

input = '''dr-of
start-KT
yj-sk
start-gb
of-start
IJ-end
VT-sk
end-sk
VT-km
KT-end
IJ-of
dr-IJ
yj-IJ
KT-yj
gb-VT
dr-yj
VT-of
PZ-dr
KT-of
KT-gb
of-gb
dr-sk
dr-VT'''

# number of distinct paths that start at start, end at end, and don't visit small caves more than once

from collections import defaultdict, Counter

connections = None

def load_data(data):
    global connections
    connections = defaultdict(set)
    for line in data.split('\n'):
        a,b = line.split('-')
        connections[a].add(b)
        connections[b].add(a)

def path_counts2(path, visit_counter):
    result = 0
    for i in connections[path[-1]]:
        if i == 'start':
            continue
        if i == 'end':
            result += 1
            continue
        if i.islower() and visit_counter[i]:
            [(_,cnt)] = visit_counter.most_common(1)
            if cnt > 1:
                continue
        path.append(i)
        if i.islower():
            visit_counter[i] += 1
        result += path_counts2(path, visit_counter)
    end = path.pop()
    if end.islower():
        visit_counter[end] -= 1
    return result

load_data(test1)
print(path_counts2(['start'], Counter(['start'])))
load_data(test2)
print(path_counts2(['start'], Counter(['start'])))
load_data(test3)
print(path_counts2(['start'], Counter(['start'])))
load_data(input)
print(path_counts2(['start'], Counter(['start'])))

exit(0)

def path_counts1(path, visit_counter):
    result = 0
    for i in connections[path[-1]]:
        if i == 'end':
            result += 1
            continue
        if i.islower() and visit_counter[i]:
            continue
        path.append(i)
        visit_counter[i] += 1
        result += path_counts1(path, visit_counter)
    end = path.pop()
    visit_counter[end] -= 1
    return result

load_data(test1)
print(path_counts1(['start'], Counter(['start','start'])))
load_data(test2)
print(path_counts1(['start'], Counter(['start','start'])))
load_data(test3)
print(path_counts1(['start'], Counter(['start','start'])))
load_data(input)
print(path_counts1(['start'], Counter(['start','start'])))






