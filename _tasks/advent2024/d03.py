import re

lines = ["xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"]
lines = [i.strip() for i in open('inputs/d03.txt').readlines()]

def mul(s):
	a, b = s.split(',')
	a = a.split('(')[1]
	b = b.split(')')[0]
	#print(s, int(a) * int(b))
	return int(a) * int(b)


s = 0
for line in lines:
	found = re.findall('mul *\\( *[0-9]{1,3} *, *[0-9]{1,3} *\\)', line)
	for m in found:
		s += mul(m)

print(s)


# II


s = 0
f = True
for line in lines:
	found = re.findall("do\\(\\)|don't\\(\\)|mul *\\( *[0-9]{1,3} *, *[0-9]{1,3} *\\)", line)
	for m in found:
		if m == "don't()":
			f = False
		elif m == "do()":
			f = True
		else:
			if f:
				s += mul(m)

print(s)