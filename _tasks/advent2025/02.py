

test = '''11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124'''
parse = lambda x: (int(x.split('-')[0]), int(x.split('-')[1]))


data = test
data = open('02.txt').readlines()[0]

data = [parse(s) for s in data.split(',')]


def invalid(i):
	s = str(i)
	return s[:len(s)//2] == s[len(s)//2:]



s = 0
for a, b in data:
	for i in range(a, b+1):
		if invalid(i):
			s += i

print(s)

# II

import textwrap


def invalid2(i):
	s = str(i)
	for l in range(1, len(s)):
		arr = textwrap.wrap(s, l)
		if len(arr) == 1 or len(arr[0]) != len(arr[-1]):
			continue
		if all([a == b for a, b in zip(arr, arr[1:])]):
			return True
	return False


s = 0
for a, b in data:
	for i in range(a, b+1):
		if invalid2(i):
			s += i

print(s)