from utils import *

input_test = """Blueprint 1:
  Each ore robot costs 4 ore.
  Each clay robot costs 2 ore.
  Each obsidian robot costs 3 ore and 14 clay.
  Each geode robot costs 2 ore and 7 obsidian.
-
Blueprint 2:
  Each ore robot costs 2 ore.
  Each clay robot costs 3 ore.
  Each obsidian robot costs 3 ore and 8 clay.
  Each geode robot costs 3 ore and 12 obsidian."""

input_test2 = """Blueprint 1:
  Each ore robot costs 1 ore.
  Each clay robot costs 1 ore.
  Each obsidian robot costs 1 ore and 1 clay.
  Each geode robot costs 1 ore and 1 obsidian."""


input_test = ''.join(input_test.split('\n')).split('-')

input_full = open('d19.txt').readlines()

input = [l.strip() for l in input_full]  # input_full input_test
input = input[:3]


def parse_blueprint(line):
    def _parse(line):
        if 'costs ' in line:
            line = line.split('costs ')[1]
        return int(line.split(' ')[0])
    line = line.split(':')[1]
    ore, clay, obs, geo, _ = line.split('.')
    assert 'ore robot' in ore
    assert 'clay robot' in clay
    assert 'obsidian robot' in obs
    assert 'geode robot' in geo
    ore = (_parse(ore), 0, 0, 0)
    clay = (_parse(clay), 0, 0, 0)
    obs1, obs2 = obs.split(' and ')
    assert 'ore' in obs1
    assert 'clay' in obs2
    obs = (_parse(obs1), _parse(obs2), 0, 0)
    geo1, geo2 = geo.split(' and ')
    assert 'ore' in geo1
    assert 'obsidian' in geo2
    geo = (_parse(geo1), 0, _parse(geo2), 0)
    return ore, clay, obs, geo


def enough(robot_blueprint, resources):
    assert len(robot_blueprint) == len(resources)
    for i, j in zip(robot_blueprint, resources):
        if i > j:
            return False
    return True


def check_blueprint(blueprint, resources):
    res = []
    for robot_blueprint in blueprint:
        res.append(1 if enough(robot_blueprint, resources) else 0)
    return res


def spend_on_robot(robot_blueprint, resource, c=1):
    assert len(robot_blueprint) == len(resource)
    for i in range(len(robot_blueprint)):
        resource[i] += c * robot_blueprint[i]


TURNS = 32
blueprint = parse_blueprint(input[0])
max_blueprint = [max([blueprint[j][i] for j in range(i+1, 4)]) for i in range(3)]
print(blueprint, max_blueprint)
c = 0
max_geo = 0


def step(time, robots, resources, robot_index):
    def mining(robots, resources):
        for i, r in enumerate(robots):
            resources[i] += r
    global blueprint, max_blueprint, TURNS, max_geo, c
    c += 1
    robots = list(robots)
    resources = list(resources)
    while not enough(blueprint[robot_index], resources):
        mining(robots, resources)
        time += 1
        if time > TURNS:
            max_geo = max(max_geo, resources[3])
            return resources[3]
    spend_on_robot(blueprint[robot_index], resources, -1)
    mining(robots, resources)
    robots[robot_index] += 1
    #
    time += 1
    if time > TURNS:
        max_geo = max(max_geo, resources[3])
        return resources[3]
    # drop?
    max_geo_limit = resources[3] + robots[3] * (TURNS - time + 1) + (TURNS - time + 1) * (TURNS - time) / 2
    if max_geo_limit < max_geo:
        return 0
    # next step
    res = [0]
    for new_robot in range(4):
        if new_robot != 3 and max_blueprint[new_robot] <= robots[new_robot]:
            continue
        if new_robot == 2 and not robots[1]:
            continue
        if new_robot == 3 and not robots[2]:
            continue
        res.append(step(time, robots, resources, new_robot))
    return max(res)

m = []
for line in input:
    blueprint = parse_blueprint(line)
    max_blueprint = [max([blueprint[j][i] for j in range(i+1, 4)]) for i in range(3)]
    max_geo = 0
    c = 0
    time, robots, resources = 1, [1, 0, 0, 0], [0, 0, 0, 0]
    a = step(time, robots, resources, robot_index=0)
    b = step(time, robots, resources, robot_index=1)
    m.append(max(a, b))
    print(m[-1], 'c', c)

print(m[0]*m[1]*m[2])


exit(1)












TURNS = 32
blueprint = None
robots = [[1, 0, 0, 0] for _ in range(TURNS + 1)]
resources = [[0, 0, 0, 0] for _ in range(TURNS + 1)]


robots = [[1, 0, 0, 0] for _ in range(TURNS+1)]
resources = [[0, 0, 0, 0] for _ in range(TURNS+1)]
max_geo_robots = [0 for _ in range(TURNS+1)]
single_obidian_robots = [0 for _ in range(TURNS+1)]
#building = [0 for _ in range(TURNS+1)]

c = 0


def run_step(blueprint, robots, resources, time):
    global c, max_geo_robots, max_blueprint#, building
    if False and time == 32 and (resources[time-1][3] + robots[time-1][3]) == 42:
        print('resources')
        for i in range(len(resources)):
            print(i, resources[i])
        print('\n----\n')
        print('robots')
        for i in range(len(robots)):
            print(i, robots[i])
        print('max_geo_robots', max_geo_robots)
        exit(0)
    """
    if single_obidian_robots[time-1]:
        if not robots[time-1][2]:
            return 0
    else:
        if robots[time-1][2]:
            single_obidian_robots[time - 1] = 1
    """
    if max_geo_robots[time-1] < robots[time-1][3]:
        max_geo_robots[time-1] = robots[time-1][3]
        for t in range(time, TURNS):
            if max_geo_robots[t] < robots[time - 1][3]:
                max_geo_robots[t] = robots[time - 1][3]
    if max_geo_robots[time-1] > robots[time-1][3]:
        return 0
    c+=1
    #print('IN')
    if time == TURNS:
        return resources[time-1][3] + robots[time-1][3]
    robots[time] = list(robots[time - 1])
    resources[time] = list(resources[time-1])
    # add resources
    for i, r in enumerate(robots[time]):
        resources[time][i] += r
    # add robot?
    results = [0]
    add_robots = check_blueprint(blueprint, resources[time - 1])
    # do nothing
    if not (all(add_robots[:3]) or add_robots[3]):
        results.append(run_step(blueprint, robots, resources, time + 1))
    # geodes heuristics
    #if add_robots[3]:
    #    add_robots = [0,0,0,1]
    #else:
    for i in range(3):
        if max_blueprint[i] <= robots[time-1][i]:
            add_robots[i] = 0
    # ore heuristics
    if add_robots[0]:  # ore
        if resources[time][0] > 10:
            add_robots[0] = 0
    #can_do_nothing = True
    if time > 0 and any(add_robots):
        #if building[time - 1] == 0 and building[time - 2] == 0:
        #    building[time - 1] = building[time - 2] = 1
        # add robots
        for i in range(len(robots[0])):
            if add_robots[i]:
                robots[time][i] += 1
                spend_on_robot(blueprint[i], resources[time], -1)
                results.append(run_step(blueprint, robots, resources, time + 1))
                # restore
                robots[time][i] -= 1
                spend_on_robot(blueprint[i], resources[time], +1)
        #    building[time - 1] = building[time - 2] = 0
    #print(results)
    return max(results)

"""
print(run_step(blueprint, robots, resources, 1))
blueprint = parse_blueprint(input[1])
print(run_step(blueprint, robots, resources, 1))
exit(0)

print(run_step(blueprint, robots, resources, 1))
print('TURNS',TURNS,'c', c)
blueprint = parse_blueprint(input[1])
print(run_step(blueprint, robots, resources, 1))


print('resources')
for i in range(len(resources)):
    print(i, resources[i])
print('\n----\n')
print('robots')
for i in range(len(robots)):
    print(i, robots[i])
print('max_geo_robots',max_geo_robots)
"""





quality = 0
for id, line in enumerate([line.strip() for line in input]):
    for ore, clay in [0, 1], [1, 0]:
        res = []
    blueprint = parse_blueprint(line)
    robots = [[1, 0, 0, 0] for _ in range(TURNS + 1)]
    resources = [[0, 0, 0, 0] for _ in range(TURNS + 1)]
    max_geo_robots = [0 for _ in range(TURNS + 1)]
    single_obidian_robots = [0 for _ in range(TURNS + 1)]
    #
    max_geodes = run_step(blueprint, robots, resources, 1)
    print(id+1, 'c', c, max_geodes)
    c = 0
    quality += max_geodes * (id+1)

print(quality)

# PART II

for line in [line.strip() for line in input]:
    pass