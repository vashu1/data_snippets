# count number of possible buildings of N meter high with 1 and 2 meter floors
import timeit
import functools

# recursive with cache
@functools.lru_cache(maxsize=128, typed=False)
def ending1(N):
	if N == 1:
		return 1
	if N == 2:
		return 1
	return ending1(N-2) + ending2(N-2) + ending2(N-1) #   12..21__ 12..22__ 12..22_

@functools.lru_cache(maxsize=128, typed=False)
def ending2(N):
	if N == 1:
		return 0
	if N == 2:
		return 1
	return ending1(N-2) + ending2(N-2) #   12..21__ 12..22__ 12..22_

@functools.lru_cache(maxsize=128, typed=False)
def combinations(N):
	#if N <= 0:
	#	raise ValueError(f'N should be positive {N}')
	return ending1(N) + ending2(N)

# rewrite to loop
def combinations2(N):
	# if N <= 0:
	#	raise ValueError(f'N should be positive {N}')
	ending1 = [0, 1, 1] + [0] * (N-2)
	ending2 = [0, 0, 1] + [0] * (N-2)
	for indx in range(3, N+1):
		ending1[indx] = ending1[indx-2] + ending2[indx-2] + ending2[indx-1]
		ending2[indx] = ending1[indx-2] + ending2[indx-2]
	return ending1[N] + ending2[N]

"""
ending1 = [0, 1, 1]
ending2 = [0, 0, 1]
data = list(zip(ending1, ending2))
for indx in range(3, N+1):
	ending1 = data[indx-2][0] + data[indx-2][1] + data[indx-1][1]
	ending2 = data[indx-2][0] + data[indx-2][1]
	data.append((ending1, ending2))
return sum(data[N])
"""

def test(N, correct):
	result = combinations(N)
	print(f'{N} {result} {result == correct} recursive')
	result = combinations2(N)
	print(f'{N} {result} {result == correct} loop')

print('---- combinations')
test(1, 1) # 1: 1
test(2, 2) # 2: 11 2
test(3, 3) # 3: 111 12 21
test(4, 5) # 5: 1111 22 211 1221 112
test(5, 8) # 8: 11111 2111 1211 1121 1112 221 212 122

print('\n--- performance')
N = 32
print(f'time for N={N}: {timeit.timeit(stmt=lambda: combinations(N), number=1)}')
N = 40
print(f'time for N={N}: {timeit.timeit(stmt=lambda: combinations(N), number=1)}')
N = 200
print(f'time for N={N}: {timeit.timeit(stmt=lambda: combinations(N), number=1)}')
print(f'200 = {combinations(200)}')

print('\n\nEXTRA:')
print('---- ending1')
def test1(N, correct):
	result = ending1(N)
	print(f'{N} {result} {result == correct}')

test1(3, 2) # 2: 111 21
test1(4, 3) # 3: 1111 211 1221

print('---- ending2')
def test2(N, correct):
	result = ending2(N)
	print(f'{N} {result} {result == correct}')

test2(3, 1) # 1: 12
test2(4, 2) # 2: 22 12

