
test = '''aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out'''

data = test.split('\n')
data = [s.strip() for s in open('11.txt').readlines()]

links = {}
for line in data:
	s, dsts = line.split(': ')
	links[s] = dsts.split(' ')
	assert s not in links[s]


def run(links, head, tail=set(), to='out', visit=set(), r=set()):
	if head == to:
		for i in visit:
			if i not in tail:
				return 0
		return 1
	s = 0
	tail.add(head)
	for i in links[head]:
		if i in tail:
			continue
		if r and i not in r:
			return 0
		s += run(links, i, tail, to, visit)
		if s % 1_000 == 999:
			print(s)
	tail.remove(head)
	return s


print(run(links, 'you'))

# II

from collections import defaultdict

test = '''svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out'''


def reachable(links, end):
	revert = defaultdict(list)
	for k in links:
		for k2 in links[k]:
			revert[k2].append(k)
	res_list = [end]
	res_set = set(res_list)
	indx = 0
	while indx < len(res_list):
		for i in revert[res_list[indx]]:
			if i not in res_set:
				res_set.add(i)
				res_list.append(i)
		indx += 1
	return res_set


data = test.split('\n')
data = [s.strip() for s in open('11.txt').readlines()]

links = {}
links['out'] = []
for line in data:
	s, dsts = line.split(': ')
	links[s] = dsts.split(' ')
	assert s not in links[s]


order = []
for i in links:
	order.append((len(reachable(links, i)), i))

order.sort(key = lambda x: x[0])
for a, b in zip(order, order[1:]):
	v1, _ = a
	v2, _ = b
	if abs(v1 - v2) > 3:
		print(v1 - v2, a, b)

#print(run(links, 'svr', set(), set(['dac', 'fft'])))
#print(run(links, 'svr', to='dac'))
print(run(links, 'kgm', to='gqx', r=reachable(links, 'gqx')))
print(run(links, 'svr', to='kgm', r=reachable(links, 'kgm')))

exit()
print(run(links, 'svr', to='fft', r=reachable(links, 'fft')))
print(run(links, 'dac', to='fft'))  # == 0
print(run(links, 'fft', to='dac', r=reachable(links, 'dac')))
print(run(links, 'dac', to='out', r=reachable(links, 'out')))  # == 3420     so it is: svr -> fft -> dac -3420-> out
#print(run(links, 'fft', to='out'))



#lru_cache 
#If you want unlimited size you can use the equivalent below ( @lru_cache(maxsize=None) == @cache, it's a shortcut for the same thing.)
#from functools import cache
