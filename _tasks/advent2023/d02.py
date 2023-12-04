from collections import Counter


def extract(line):
	c = Counter()
	for i in line.split(', '):
		i = i.strip()
		n, color = i.split(' ')
		n = int(n)
		c[color] = n
	return (c['red'], c['green'], c['blue'])


def cmp(bag, step):
	return all([i >= j for i, j in zip(bag, step)])


bag = extract('12 red, 13 green, 14 blue')
lines = '''Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green'''.split('\n')

bag = extract('12 red, 13 green, 14 blue')
lines = [l.strip() for l in open('d02.txt').readlines()]

s = 0
for line in lines:
	game_num, data = line.split(': ')
	game_num = int(game_num.split(' ')[1])
	res = [cmp(bag, extract(step)) for step in data.split(';')]
	res = all(res)
	if res:
		#print(game_num)
		s += game_num

print('sum', s)


# 2


s = 0
for line in lines:
	game_num, data = line.split(': ')
	game_num = int(game_num.split(' ')[1])
	res = [extract(step) for step in data.split(';')]
	res = list(map(max, [j for j in zip(*res)]))
	m = res[0]*res[1]*res[2]
	s += m

print(s)