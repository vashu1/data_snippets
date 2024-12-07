lines = '''190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20'''
lines = lines.split('\n')
lines = [i.strip() for i in open('d07.txt').readlines()]


cnt = 0
for line in lines:
	v, eq = line.split(': ')
	v = int(v)
	eq = [int(i) for i in eq.split(' ')]
	l = len(eq) - 1
	for i in range(2 ** l):  # max - 12 terms
		ops = f'{i:b}'.zfill(l)
		acc = eq[0]
		for indx, op in enumerate(ops):
			if ops[indx] == '1':
				acc += eq[indx + 1]
			else:
				acc *= eq[indx + 1]
		if acc == v:
			cnt += v
			break

print(cnt)