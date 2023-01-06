volume = 150
data = []

for line in open('d17.txt').readlines():
    line = line.strip()
    data.append(int(line))

# test data
#volume = 25
#data = [20, 15, 10, 5, 5]

data.sort(reverse=True)

sum_next = [sum(data[i:]) for i in range(len(data) + 1)]

c = 0  # count calc() calls
vals = []  # all good container combinations
stack = []  # current container indexes
cache = {}
def calc(index, current_volume):
    #if (index, current_volume) in cache:  # cache 25K calls -> 3K, but we cannot use cache for part2
    #    return cache[(index, current_volume)]
    global c
    c += 1
    current_volume -= data[index]
    stack.append(data[index])
    if current_volume == 0:
        vals.append(tuple(stack))
        _ = stack.pop()
        return 1
    if current_volume < 0:
        _ = stack.pop()
        return 0
    s = 0
    for i in range(index + 1, len(data)):
        s += calc(i, current_volume)
        if sum_next[i] < current_volume:
            break
    _ = stack.pop()
    cache[(index, current_volume)] = s
    return s

s = 0
for i in range(len(data)):
    s += calc(i, volume)

print(s, c)

# ---------------

print('PART II')
mn = min([len(i) for i in vals])
print(len([1 for i in vals if len(i) == mn]))