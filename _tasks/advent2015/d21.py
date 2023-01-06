import itertools

shop = """Weapons:    Cost  Damage  Armor
Dagger        8     4       0
Shortsword   10     5       0
Warhammer    25     6       0
Longsword    40     7       0
Greataxe     74     8       0

Armor:      Cost  Damage  Armor
Leather      13     0       1
Chainmail    31     0       2
Splintmail   53     0       3
Bandedmail   75     0       4
Platemail   102     0       5

Rings:      Cost  Damage  Armor
Damage +1    25     1       0
Damage +2    50     2       0
Damage +3   100     3       0
Defense +1   20     0       1
Defense +2   40     0       2
Defense +3   80     0       3"""

boss = """Hit Points: 103
Damage: 9
Armor: 2"""

shop = shop.split('\n\n')

# You have 100 hit points.
# exactly one weapon; no dual-wielding. Armor is optional, but you can't use more than one.
# You can buy 0-2 rings (at most one for each hand).


def parse(line):
    line = [i for i in line.split(' ') if i]
    return int(line[-3]), int(line[-2]), int(line[-1])


weapons = {}
for line in shop[0].split('\n')[1:]:
    weapons[line] = parse(line)

armors = {'no armor': (0, 0, 0)}
for line in shop[1].split('\n')[1:]:
    armors[line] = parse(line)

rings = {}
for line in shop[2].split('\n')[1:]:
    rings[line] = parse(line)

ring_names = list(sorted(rings.keys()))

print(f'{weapons=}')
print(f'{armors=}')
print(f'{rings=}')


def run(you, boss):
    def attack(damage, armor):
        return 1 if damage <= armor else (damage - armor)
    yh, yd, ya = you
    bh, bd, ba = boss
    while True:
        bh -= attack(yd, ba)
        if bh <= 0:
            return True
        yh -= attack(bd, ya)
        if yh <= 0:
            return False


results = []
for weapon in weapons:
    for armor in armors:
        for ring_count in range(2 + 1):
            for ring_combo in itertools.combinations(range(6), ring_count):
                inventory_names = [weapon, armor]
                inventory = [weapons[weapon], armors[armor]]
                for ring in ring_combo:
                    ring_name = ring_names[ring]
                    inventory_names.append(ring_name)
                    inventory.append(rings[ring_name])
                cost, yd, ya = map(sum, zip(*inventory))
                you = (100, yd, ya)
                boss = (103, 9, 2)
                r = run(you, boss)
                results.append((r, cost, inventory_names))

# print results

print('\nPART I\n')
print(len(results))
results2 = [(c, i) for r, c, i in results if r]
print(len(results2))
print('\n\n\n')
results2.sort(key=lambda k: k[0])
print(results2[0])
print(results2[1])
print(results2[2])
print(results2[3])
print(results2[4])

print('\n\n\n')
print(results2[0][0])

print('\n\n\nPART II\n')
print(len(results))
results2 = [(c, i) for r, c, i in results if not r]
print(len(results2))
print('\n\n\n')
results2.sort(key=lambda k: k[0], reverse=True)
print(results2[0])
print(results2[1])
print(results2[2])
print(results2[3])
print(results2[4])

print('\n\n\n')
print(results2[0][0])
