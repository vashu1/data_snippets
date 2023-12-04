

lines = '''Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11'''.split('\n')

lines = [l.strip() for l in open('d04.txt').readlines()]

s = 0
for line in lines:
	line = line.split(': ')[1]
	a, b = line.split('|')
	a = [int(i) for i in a.split(' ') if i]
	b = [int(i) for i in b.split(' ') if i]
	a = set(a)
	b = set(b)
	wins = a.intersection(b)
	if wins:
		score = 2 ** (len(wins) - 1)
		#print(score, wins)
		s += score

print('sum', s)

# 2

c = 1
graph = {}
for line in lines:
	line = line.split(': ')[1]
	a, b = line.split('|')
	a = [int(i) for i in a.split(' ') if i]
	b = [int(i) for i in b.split(' ') if i]
	a = set(a)
	b = set(b)
	wins = a.intersection(b)
	if wins:
		graph[c] = set(range(c + 1, c + len(wins) + 1))
	c += 1


value = {}
for i in range(len(lines), 0, -1):
	value[i] = 1 + sum([value[j] for j in graph.get(i, [])])

print('sum', sum(value.values()))