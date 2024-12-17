lines = '''Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0'''
lines = '''Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0'''
lines = lines.split('\n')
lines = [i.strip() for i in open('inputs/d17.txt').readlines()]

A, B, C = 0, 1, 2
registers = []
for i in range(3):
	registers.append(int(lines[i].split(' ')[-1]))

instruction_p = 0
program = [int(i) for i in lines[4].split(' ')[1].split(',')]
result = []

def combo():
	global program, instruction_p, registers, result
	p = program[instruction_p + 1] % 8
	if p in [0, 1, 2, 3]:
		return p
	elif p in [4, 5, 6]:
		return registers[p - 4] % 8
	elif p == 7:
		assert False
	assert p < 8


def run_step():
	global program, instruction_p, registers, result
	if program[instruction_p] == 0:
		registers[A] //= 2 ** combo()
	elif program[instruction_p] == 1:
		registers[B] ^= program[instruction_p + 1]
	elif program[instruction_p] == 2:
		registers[B] = combo()
	elif program[instruction_p] == 3:
		if registers[A] != 0:
			instruction_p = program[instruction_p + 1] - 2
	elif program[instruction_p] == 4:
		registers[B] ^= registers[C]
	elif program[instruction_p] == 5:
		result.append(combo())
	elif program[instruction_p] == 6:
		registers[B] = registers[A] // (2 ** combo())
	elif program[instruction_p] == 7:
		registers[C] = registers[A] // (2 ** combo())
	else:
		assert False

'''
0,3 registers[A] //= 8
5,4 result.append(A)
3,0 if registers[A] != 0:
			instruction_p = program[instruction_p + 1] - 2

2,4 registers[B] = registers[B] % 8
1,5 registers[B] ^= 5
7,5 registers[C] = registers[A] // (2 ** registers[B] % 8)
1,6 registers[B] ^= 6
4,3 registers[B] ^= registers[C] % 8
5,5 result.append(registers[B])
3,0 if registers[A] != 0:
			instruction_p = 0


47792830
2,1,3,0,5,2,3,7,1
2,4,1,5,7,5,1,6,4,3,5,5,0,3,3,0
'''

while True:
	assert instruction_p >= 0
	if instruction_p >= len(program) - 1:
		break
	run_step()
	instruction_p += 2


print(','.join([str(i) for i in result]))

# 4,6,3,5,6,3,5,2,1,0
# 4,6,3,5,6,3,5,2,1,0

# bad 0,6,1,7,3,4,0,5,1
# good 2,1,3,0,5,2,3,7,1


# II



best = [1]
best_a = None

def score(p, v):
	n = 0
	for a, b in zip(p, v):
		if a != b:
			break
		n += 1
	return n


value_a = 0o3033075014424630 - 100_000
n = 0
while True:
	#if value_a % 1_000_000 == 0:
	#	print(program, result)
	registers = [value_a, 0, 0]
	instruction_p = 0
	result = []
	while True:
		assert instruction_p >= 0
		if instruction_p >= len(program) - 1:
			break
		run_step()
		instruction_p += 2
	if n > 1_000_000:
		break
	n += 1
	p = list(reversed(program))
	r = list(reversed(result))
	b = score(p, best)
	rr = score(p, r)
	if rr > b:
		best = r
		best_a = value_a
	value_a += 1


print(p)
print(best)
print(best_a)


# 166000000