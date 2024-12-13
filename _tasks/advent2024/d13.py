lines = '''Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279'''
lines = lines.split('\n')
lines = [i.strip() for i in open('d13.txt').readlines()]


def solution(ax, ay, bx, by, px, py):
	solutions = []
	a = 0
	while True:
		sx = px - a * ax
		sy = py - a * ay
		if sx < 0 or sy < 0:
			break
		if sx % bx == 0 and sy % by == 0:
			sx = sx // bx
			sy = sy // by
			if sx == sy:
				b = sx
				assert a <= 100 and b <= 100
				solutions.append((a, b))
		a += 1
	return solutions


def solution2(ax, ay, bx, by, px, py):
	b = (ay * px - ax * py) // (ay * bx - ax * by)
	if (ay * px - ax * py) % (ay * bx - ax * by) != 0 or b < 0:
		return []
	a = (px - bx * b) // ax
	if (px - bx * b) % ax != 0 or a < 0:
		return []
	return [a, b]


def extract(line):
	x, y = line.split(': ')[1].split(', ')
	return int(x[2:]), int(y[2:])


cost = cost2 = 0
lines.append('')
for line in lines:
	if line.startswith('Button A: '):
		ax, ay = extract(line)
	if line.startswith('Button B: '):
		bx, by = extract(line)
	if line.startswith('Prize: '):
		px, py = extract(line)
	if line == '':
		costs = [3 * a + b for a, b in solution(ax, ay, bx, by, px, py)]
		if costs:
			cost += min(costs)
		px += 10000000000000  # 10^13
		py += 10000000000000
		costs = solution2(ax, ay, bx, by, px, py)
		if costs:
			a, b = costs
			cost2 += 3 * a + b

print(cost)
print(cost2)