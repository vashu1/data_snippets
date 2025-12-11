
test = '''.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
...............'''

data = test.split('\n')
data = [s.strip() for s in open('07.txt').readlines()]

s = 0
data = [list(line) for line in data]
cnt = [[0]*len(data[0]) for _ in range(len(data))]
cnt[0][data[0].index('S')] = 1
for i in range(1, len(data)):
	for j in range(len(data[0])):
		assert len(data[0]) == len(data[j])
		if data[i-1][j] == 'S':
			if data[i][j] == '^':
				assert data[i][j-1] != '^' and data[i][j+1] != '^'
				data[i][j-1] = 'S'
				data[i][j+1] = 'S'
				cnt[i][j-1] += cnt[i-1][j]
				cnt[i][j+1] += cnt[i-1][j]
				s += 1
			else:
				data[i][j] = 'S'
				cnt[i][j] += cnt[i-1][j]

print(s)

# II

print(sum(cnt[-1]))