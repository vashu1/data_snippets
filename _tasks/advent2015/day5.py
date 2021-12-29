vowels = 'aeiou'
bad_bigrams = ['ab', 'cd', 'pq', 'xy']

lines = [line.strip() for line in open('input5.txt').readlines()]
total = 0
for line in lines:
    vowels_count = len([c for c in line if c in vowels])
    double_count = len([a+b for a,b in zip(line[:-1], line[1:]) if a==b])
    third_condition = any([s in line for s in bad_bigrams])
    if vowels_count >= 3 and double_count>0 and not third_condition:
        total += 1

print('task1', total)

total = 0
for line in lines:
    cond1 = len([(i, j) for i in range(len(line)-1)
        for j in range(i+2, len(line)-1)
            if line[i:i+2] == line[j:j+2]]) > 0
    cond2 = len([line[i:i+3] for i in range(len(line)-2) if line[i] == line[i+2]]) > 0
    if cond1 and cond2:
        total += 1

print('task2', total)