from collections import defaultdict

lines = '''47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47'''
lines = lines.split('\n')
lines = [i.strip() for i in open('d05.txt').readlines()]

#s = set()
pairs = defaultdict(set)
cnt = 0
incorrects = []
for line in lines:
	if not line:
		continue
	if '|' in line:  # rule    X|Y   page number X must be printed at some point before page number Y
		x, y = line.split('|')
		x = int(x)
		y = int(y)
		#s.add(x)
		#s.add(y)
		pairs[x].add(y)
	if ',' in line:
		update = [int(i) for i in line.split(',')]
		#if not all([i in s for i in update]):
		#	print('error')
		assert len(update) % 2 == 1, len(update)
		correct = True
		for i in range(len(update)):
			for j in range(i):
				# y|x case
				if update[j] in pairs.get(update[i], set()):
					correct = False
		if correct:
			cnt += update[len(update)//2]
		else:
			incorrects.append(update)


print(cnt)


# II


def fix(update):
	for i in range(len(update)):
		for j in range(i):
			if update[j] in pairs.get(update[i], set()):
				update[i], update[j] = update[j], update[i]
				return False
	return True


cnt = 0
for update in incorrects:
	while fix(update):
		pass
	cnt += update[(len(update)-1)//2]

print(cnt)