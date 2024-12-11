import functools

lines = '''125 17'''
lines = lines.split('\n')
lines = [i.strip() for i in open('d11.txt').readlines()]
data = [int(i) for i in lines[0].split(' ')]


def change(i):
	s = str(i)
	if i == 0:
		i = 1
		return [i]
	elif len(s) % 2 == 0:
		return [int(s[:len(s) // 2]), int(s[len(s) // 2:])]
	else:
		return [i * 2024]


def flatten(lst):
    return [item for sublist in lst for item in sublist]


def blink(lst):
	res = [change(i) for i in lst]
	return flatten(res)


for i in range(25):
	data = blink(data)

print(len(data))



# II


@functools.lru_cache(maxsize=None)
def change_depth(i, depth):
	s = str(i)
	res = None
	if i == 0:
		i = 1
		res = [i]
	elif len(s) % 2 == 0:
		res = [int(s[:len(s) // 2]), int(s[len(s) // 2:])]
	else:
		res = [i * 2024]
	if depth == 1:
		res = len(res)
	else:
		res = sum([change_depth(j, depth-1) for j in res])
	return res


data = [int(i) for i in lines[0].split(' ')]
print(sum([change_depth(i, 75) for i in data]))
