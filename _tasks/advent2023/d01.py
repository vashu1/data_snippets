
def extract(line):
	line = [c for c in line if c.isdigit()]
	#print(line, int(line[0] + line[-1]))
	assert len(line) > 0  # 1 is ok
	return int(line[0] + line[-1])

lines = '''1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet'''.split('\n')

lines = open('d01.txt').readlines()

print(sum([extract(line) for line in lines]))



REPLACE = {
	'one':   1,
	'two':   2,
	'three': 3,
	'four':  4,
	'five':  5,
	'six':   6,
	'seven': 7,
	'eight': 8,
	'nine':  9,
}

def fix(line):
	for k, v in REPLACE.items():
		line = line.replace(k, k+str(v)+k)
	return line

lines2 = '''two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen'''.split('\n')


print(sum([extract(fix(line)) for line in lines]))