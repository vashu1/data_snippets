from collections import defaultdict, Counter
import itertools
import parse

test = """Alice would gain 54 happiness units by sitting next to Bob.
Alice would lose 79 happiness units by sitting next to Carol.
Alice would lose 2 happiness units by sitting next to David.
Bob would gain 83 happiness units by sitting next to Alice.
Bob would lose 7 happiness units by sitting next to Carol.
Bob would lose 63 happiness units by sitting next to David.
Carol would lose 62 happiness units by sitting next to Alice.
Carol would gain 60 happiness units by sitting next to Bob.
Carol would gain 55 happiness units by sitting next to David.
David would gain 46 happiness units by sitting next to Alice.
David would lose 7 happiness units by sitting next to Bob.
David would gain 41 happiness units by sitting next to Carol."""

data = defaultdict(Counter)
persons = set()

#for line in test.split('\n'):
for line in open('d13.txt').readlines():
    line = line.strip()
    p1, c, value, p2 = parse.parse('{} would {} {:d} happiness units by sitting next to {}.', line)
    assert c in ['gain', 'lose']
    c = 1 if 'gain' == c else -1
    data[p1][p2] = c * value
    persons.add(p1)
    persons.add(p2)


def rotated_1_left(lst):  # [1, 2, 3] -> [2, 3, 1]
    for i in lst[1:]:
        yield i
    if lst:
        yield lst[0]


def process():
    c = 0
    mx = -1
    for seating in itertools.permutations(persons, len(persons)):
        c += 1
        s = 0
        for p1, p2 in zip(seating, rotated_1_left(seating)):
            s += data[p1][p2]
            s += data[p2][p1]
        mx = max(mx, s)

    print(c, mx)


process()

# part 2
persons.add('me')
process()
