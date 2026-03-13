'''
All numbers from 1 to N, except one, are shuffled in random order and written consecutively without spaces.

You are given this string and must determine which number is missing.
'''
import random
from collections import Counter
import itertools

#N = 90
#EXCLUDE = 54
SEED = 1

DELIM = '|'


def flatten(lst):
    return [item for sublist in lst for item in sublist]


'''
def split(list_of_strings, drop):
	f = lambda sequence, drop: [sequence] if drop not in sequence else [sequence[:sequence.index(drop)], sequence[sequence.index(drop)+len(drop):]]
	list_of_strings = [f(sequence, drop) for sequence in list_of_strings]
	list_of_strings = flatten(list_of_strings)
	list_of_strings = [i for i in list_of_strings if i]  # drop empty
	return list_of_strings
'''


def is_ok(sequence, val, others):
	sequence = DELIM + sequence + DELIM
	# extract counts from sequence
	while True:
		c = Counter()
		places = {}
		for indx in range(len(sequence)):
			for l in range(1, LN + 1):
				s = sequence[indx:indx+l]
				if len(s) < l or s not in others or DELIM in s:
					continue
				c[s] += 1
				places[s] = indx
		#print(c, LN)
		#print([(k, v) for k, v in c.most_common() if v == 1]) # k in others and
		for i in others:
			if i not in c:
				#print(i, 'i not in c', sequence, others)
				return False
		# drop doublets
		drops = [k for k, v in c.most_common() if v == 2]
		f = False
		for drop in drops:
			d = DELIM + drop + DELIM
			if d in sequence:
				sequence = sequence.replace(d, DELIM, 1)
				others.remove(drop)
				f = True
		if f:
			continue
		# drop singles
		splits1 = [(k, v) for k, v in c.most_common() if v == 1 and val not in k]
		splits2 = [(k, v) for k, v in c.most_common() if v == 1]
		splits = splits1 if splits1 else splits2
		if not splits:
			for l in range(LN, 0, -1):
				for k, _ in c.most_common():
					if len(k) != l:
						continue
					if k in sequence:
						#print('last chance drop', k, sequence)
						sequence = sequence.replace(k, DELIM, 1)
						others.remove(k)
			if not [ch for ch in sequence if ch != DELIM]:
				#print('OK')
				return True
			#print(i, 'not splits', c, others)
			return False
		for split, _ in splits:
			#print(sequence, split)
			sequence = sequence.replace(split, DELIM, 1)
			others.remove(split)
		# single drop
		#drop = splits[0][0]
		#print('DROP', drop)
		#sequences = split(sequences, drop)
		#print(sequences, others)
		#others.remove(drop)
		if not [ch for ch in sequence if ch != DELIM]:
			#print('OK')
			return True
	

for N in [15,99]:
	for EXCLUDE in range(1, N):
		#print('\n\n\n\n')
		LN = len(str(N))  # how many digits can be in a number

		sequence = set([i for i in range(1, N + 1)])
		sequence.remove(EXCLUDE)
		sequence = list(sequence)
		random.seed(SEED)
		random.shuffle(sequence)
		sequence = ''.join([str(i) for i in sequence])

		#TODO if N is not known - recover value of N from sequence

		# recover digits of EXCLUDE
		c1 = Counter()
		for i in sequence:
			c1[i] += 1

		c2 = Counter()
		for i in range(1, N + 1):
			for j in str(i):
				c2[j] += 1

		res = c2 - c1
		nums = []
		for k, v in (c2 - c1).most_common():
			nums += [k] * v

		nums = list(set(itertools.permutations(nums)))
		nums = [''.join(i) for i in nums]
		nums = [i for i in nums if int(i) <= N]
		nums = [i for i in nums if i[0] != '0']
		#print(f'{nums}')

		res = set()
		for val in nums:
			#print(f'{val=}', sequence)
			others = set([str(i) for i in range(1, N + 1)])
			others.remove(val)
			if is_ok(sequence, val, others):
				res.add(val)
				#print('res', res)
				#print(f'{val} is ok')
			else:
				#print(f'{val} rejected')
				pass
		assert str(EXCLUDE) in res, str(res) + ' ' + str(EXCLUDE)
		if len(res) > 1:
			print(f'MULTIPLE {N=} {EXCLUDE=} {res=}')


# TODO - linear not quadratic - multi splits    drop = splits[0][0]
# process remnants  if several combinations     ['111414'] {'11', '4', '13', '14', '1'} 
#												111    Counter({'1': 3, '11': 2}) {'1', '11'}
