
lines = '''029A
980A
179A
456A
379A'''
lines = lines.split('\n')
#lines = [i.strip() for i in open('inputs/d21.txt').readlines()]


def add(state, v):
	x, y = state
	xv, yv = v
	return x + xv, y + yv


class Keyboard():
	def __init__(self, object_):
		self.object = object_
		self.state = self.INITIAL_STATE
		assert self.value() == 'A'
		self.reset_optimal_flags()

	def reset_optimal_flags(self):
		self.left = False
		self.right = False
		self.up = False
		self.down = False

	def step(self, s):
		if s == 'A':
			if self.valid_state():
				self.object.step(self.value())
			self.reset_optimal_flags()
		elif s == 'v':
			self.state = add(self.state, (0, +1))
			self.down = True
		elif s == '^':
			self.state = add(self.state, (0, -1))
			self.up = True
		elif s == '<':
			self.state = add(self.state, (-1, 0))
			self.left = True
		elif s == '>':
			self.state = add(self.state, (+1, 0))
			self.right = True

	def value(self):
		x, y = self.state
		return self.LAYOUT[y][x]

	def valid_state(self, recursive=False):
		x, y = self.state
		if not (0 <= x < len(self.LAYOUT[0])):
			return False
		if not (0 <= y < len(self.LAYOUT)):
			return False
		if self.LAYOUT[y][x] is None:
			return False
		if recursive:
			return True and self.object.valid_state()
		else:
			return True

	def optimal(self, recursive=False):
		if self.left and self.right:
			return False
		if self.up and self.down:
			return False
		if recursive:
			return True and self.object.optimal()
		else:
			return True

class NumericKeypad(Keyboard):
	INITIAL_STATE = (2, 3)
	LAYOUT = [
		['7', '8', '9'],
		['4',  '5', '6'],
		['1',  '2', '3'],
		[None, '0', 'A'],
	]

class DirectionalKeypad(Keyboard):
	INITIAL_STATE = (2, 0)
	LAYOUT = [
			[None, '^', 'A'],
			['<',  'v', '>'],
	]

class Output():
	def __init__(self):
		self.buffer = []

	def step(self, s):
		self.buffer.append(s)

	def output(self):
		return ''.join(self.buffer)


def expand_sequences(sequences):
	res = []
	for s in sequences:
		for i in ['A', 'v', '^', '<', '>']:
			res.append(s + i)
	return res


def complexity(code, sequence):
	l = len(sequence)
	i = int(''.join([ch for ch in code if ch.isdigit()]))
	return l * i


print(len('<v<A>>^A<vA<A>>^AAvAA<^A>A<v<A>>^AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A'), len('v<A<AA>^>AAvA^<A>AvA^Av<<A>^>AAvA^Av<A^>AA<A>Av<A<A>^>AAAvA^<A>A'))

solution = {
	'029A': '<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A',
	'980A': '<v<A>>^AAAvA^A<vA<AA>>^AvAA<^A>A<v<A>A>^AAAvA<^A>A<vA>^A<A>A',
	#'179A': '<v<A>>^A<vA<A>>^AAvAA<^A>A<v<A>>^AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A',
     '179A': 'v<A<AA>^>AAvA^<A>AvA^Av<<A>^>AAvA^Av<A^>AA<A>Av<A<A>^>AAAvA^<A>A',
	#'456A': '<v<A>>^AA<vA<A>>^AAvAA<^A>A<vA>^A<A>A<vA>^A<A>A<v<A>A>^AAvA<^A>A',
	'456A': 'v<A<AA>^>AAvA^<A>AAvA^Av<A^>A<A>Av<A^>A<A>Av<A<A>^>AAvA^<A>A',
	'379A': '<v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A',
}
for code in solution:
	o = Output()
	n = NumericKeypad(o)
	r1 = DirectionalKeypad(n)
	r2 = DirectionalKeypad(r1)
	bad = False
	for s in solution[code]:
		#print(s)
		#print('NumericKeypad', n.state, n.valid_state(), n.optimal(), 'robot1', r1.state, r1.valid_state(), r1.optimal(), 'robot2', r2.state, r2.valid_state(), r2.optimal())
		r2.step(s)
		if not r2.valid_state(recursive=True):
			bad = True
			print('BAD valid_state')
			break
		if not r2.optimal(recursive=True):
			bad = True
			print('BAD optimal')
			break
	print(code, o.output())
exit()


print(68 * 29 + 60 * 980 + 68 * 179 + 64 * 456 + 64 * 379 , 68 * 29, 60 * 980, 68 * 179, 64 * 456, 64 * 379)
cnt = 0
for code in lines:
	targets = {code[:i]: None for i in range(1, len(code) + 1)}
	sequences = ['']
	while True:
		sequences = expand_sequences(sequences)
		update = []
		for sequence in sequences:
			o = Output()
			n = NumericKeypad(o)
			r1 = DirectionalKeypad(n)
			r2 = DirectionalKeypad(r1)
			bad = False
			for s in sequence:
				r2.step(s)
				if not r2.valid_state(recursive=True):
					bad = True
					break
				if not r2.optimal(recursive=True):
					bad = True
					break
			if not bad:
				update.append(sequence)
			if o.output() in targets and targets[o.output()] is None:
				targets[o.output()] = sequence
				update = [sequence]
				break
		sequences = update
		#print(len(sequences), len(sequences[0]), len(sequences[-1]))
		if targets[code] is not None:
			print(code, complexity(code, targets[code]), targets[code])
			cnt += complexity(code, targets[code])
			break


print(cnt)
