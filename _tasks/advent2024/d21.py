from pygments import console
import functools
from collections import defaultdict

lines = '''029A
980A
179A
456A
379A'''
lines = lines.split('\n')
lines = [i.strip() for i in open('inputs/d21.txt').readlines()]


def prith_char(ch, colored=False):
	ch = ' ' if ch is None else ch
	if colored:
		ch = console.colorize("red", ch)
	return ch


def add(state, v):
	x, y = state
	xv, yv = v
	return x + xv, y + yv


def flatten(lst):
    return [item for sublist in lst for item in sublist]


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

	def valid_state(self):
		x, y = self.state
		if not (0 <= x < len(self.LAYOUT[0])):
			return False
		if not (0 <= y < len(self.LAYOUT)):
			return False
		if self.LAYOUT[y][x] is None:
			return False
		return True and self.object.valid_state()


	def optimal(self):
		if self.left and self.right:
			return False
		if self.up and self.down:
			return False
		return True and self.object.optimal()


	def print(self):
		for y, line in enumerate(self.LAYOUT):
			#for x, ch in enumerate(line):
			print('\t'.join([prith_char(ch, colored=self.state == (x, y)) for x, ch in enumerate(line)]))

	def key_number(self):
		return len([i for i in flatten(self.LAYOUT) if i is not None])


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

	def valid_state(self):
		return True

	def optimal(self):
		return True


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

'''
print(len('<v<A>>^A<vA<A>>^AAvAA<^A>A<v<A>>^AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A'), len('v<A<AA>^>AAvA^<A>AvA^Av<<A>^>AAvA^Av<A^>AA<A>Av<A<A>^>AAAvA^<A>A'))

solution = {
	'029A': '<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A',
	#'980A': '<v<A>>^AAAvA^A<vA<AA>>^AvAA<^A>A<v<A>A>^AAAvA<^A>A<vA>^A<A>A',
	#'179A': '<v<A>>^A<vA<A>>^AAvAA<^A>A<v<A>>^AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A',  # 68
	#'456A': '<v<A>>^AA<vA<A>>^AAvAA<^A>A<vA>^A<A>A<vA>^A<A>A<v<A>A>^AAvA<^A>A', # 64
	#'379A': '<v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A',
}
for code in solution:
	o = Output()
	n = NumericKeypad(o)
	r1 = DirectionalKeypad(n)
	r2 = DirectionalKeypad(r1)
	bad = False
	for indx, s in enumerate(solution[code]):
		#print(s)
		#print('NumericKeypad', n.state, n.valid_state(), n.optimal(), 'robot1', r1.state, r1.valid_state(), r1.optimal(), 'robot2', r2.state, r2.valid_state(), r2.optimal())
		r2.step(s)
		if not r2.valid_state():
			bad = True
			print('BAD valid_state')
			break
		if not r2.optimal():
			bad = True
			print('BAD optimal')
			break
		print('\n\n\n\n\n\n')
		n.print()
		print('\n\n')
		r1.print()
		print('\n\n')
		r2.print()
		print('\n', indx + 1, s, '       :', o.output())
		_ = input()

	print(code, o.output())
exit()
'''

#print(68 * 29 + 60 * 980 + 68 * 179 + 64 * 456 + 64 * 379 , 68 * 29, 60 * 980, 68 * 179, 64 * 456, 64 * 379)

'''
cnt = 0
solutions = {}
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
				if not r2.valid_state():
					bad = True
					break
				if not r2.optimal():
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
			solutions[code] = targets[code]
			break


print(cnt)
'''


# II





def one_step(DestinationClass):
	result = defaultdict(dict)
	for y, line in enumerate(DestinationClass.LAYOUT):
		for x, ch in enumerate(line):
			if ch is None:
				continue
			sequences = ['']
			while True:
				sequences = expand_sequences(sequences)
				update = []
				for sequence in sequences:
					o = Output()
					r1 = DestinationClass(o)
					r1.state = (x, y)
					r2 = DirectionalKeypad(r1)
					bad = False
					for s in sequence:
						r2.step(s)
						if not r2.valid_state():
							bad = True
							break
						if not r2.optimal():
							bad = True
							break
					if not bad:
						update.append(sequence)
					out = o.output()
					if len(out) == 1 and out not in result[ch]:
						result[ch][out] = sequence
				sequences = update
				if len(result[ch]) == r1.key_number():
					break
	return result


dir_num_solutions = one_step(NumericKeypad)
dir_dir_solutions = one_step(DirectionalKeypad)
print(dir_num_solutions)
print(dir_dir_solutions)

print(68 * 29 + 60 * 980 + 68 * 179 + 64 * 456 + 64 * 379 , 68 * 29, 60 * 980, 68 * 179, 64 * 456, 64 * 379)


def expand_code(code, dir_num_solutions):
	state = 'A'
	result = []
	for ch in code:
		result.append(dir_num_solutions[state][ch])
		state = result[-1][-1]
	return ''.join(result)


@functools.lru_cache(maxsize=None)
def calc_len(sequence, depth, start):
	z_seq = zip(start + sequence, sequence)
	if depth == 1:
		return sum([len(dir_dir_solutions[a][b]) for a, b in z_seq])
	return sum([calc_len(dir_dir_solutions[a][b], depth - 1, a) for a, b in z_seq])


cnt = 0
for code in lines:
	expanded_code = expand_code(code, dir_num_solutions)
	i = int(''.join([ch for ch in code if ch.isdigit()]))
	cnt += i * calc_len(expanded_code, 25, 'A')

print(cnt)
print(246810588779586)

'''
In summary, there are the following keypads:

    One directional keypad that you are using.
    25 directional keypads that robots are using.
    One numeric keypad (on a door) that a robot is using.
'''