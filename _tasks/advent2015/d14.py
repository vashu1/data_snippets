from collections import defaultdict, Counter
import parse

test = """Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.
Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds."""


def calc(fly_v, fly_t, rest_t, time):
    distance = 0
    while time > 0:
        distance += min(time, fly_t) * fly_v
        time -= fly_t
        time -= rest_t
    return distance

names = []
data = {}
distances = {}

#for line in test.split('\n'):
for line in open('d14.txt').readlines():
    line = line.strip()
    name, fly_v, fly_t, rest_t = parse.parse('{} can fly {:d} km/s for {:d} seconds, but then must rest for {:d} seconds.', line)
    distances[name] = calc(fly_v, fly_t, rest_t, 2503)
    data[name] = (fly_v, fly_t, rest_t)
    names.append(name)

print(distances)
print(max(distances.values()))


# part 2
scores = Counter()
state = {name: (0, fly_t, fly_v) for name, (fly_v, fly_t, _) in data.items()}
for _ in range(2503):
    # step
    for name in names:
        distance, time, speed = state[name]
        distance += speed
        time -= 1
        if time == 0:
            fly_v, fly_t, rest_t = data[name]
            if speed == 0:  # finished resting
                time, speed = fly_t, fly_v
            else:  # started resting
                time, speed = rest_t, 0
        state[name] = distance, time, speed
    # score
    best = max([distance for distance, _, _ in state.values()])
    for name, (distance, _, _) in state.items():
        if distance == best:
            scores[name] += 1

print(scores)
print(max(scores.values()))
