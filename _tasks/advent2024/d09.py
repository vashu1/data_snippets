from heapq import heappush, heappop
from collections import defaultdict

lines = '''2333133121414131402'''
lines = lines.split('\n')
lines = [i.strip() for i in open('d09.txt').readlines()]


def chcksum(ss):
	return sum([indx * s for indx, s in enumerate(ss) if s])

data = [int(c) for c in list(lines[0])]
l = sum(data)

disk = [None] * l
indx = 0
fid = 0
for i, val in enumerate(data):
	if i % 2 == 0:  # file
		for j in range(val):
			disk[indx] = fid
			indx += 1
		fid += 1
	else:  # space
		indx += val

i1 = 0
i2 = len(disk) - 1
while i1 < i2:
	while disk[i1] is not None:
		i1 += 1
	while disk[i2] is None:
		i2 -= 1
	disk[i1], disk[i2] = disk[i2], disk[i1]

disk[i1], disk[i2] = disk[i2], disk[i1]

print(chcksum(disk))


# II


file_indxs = {}
file_lens = {}
gaps = defaultdict(list)
disk = [None] * l
indx = 0
fid = 0
for i, val in enumerate(data):
	if i % 2 == 0:  # file
		file_indxs[fid] = indx
		file_lens[fid] = val
		for j in range(val):
			disk[indx] = fid
			indx += 1
		fid += 1
	else:  # space
		heappush(gaps[val], indx)
		indx += val

for fid_ in range(fid-1, 0, -1):
	position = file_indxs[fid_]
	file_len = file_lens[fid_]
	moves = []
	for gap_len in range(1, 9+1):
		if gap_len < file_len:
			continue
		if gaps[gap_len] == []:
			continue
		move_indx = gaps[gap_len][0]
		if move_indx > position:
			continue
		moves.append((move_indx, gap_len))
	if moves:
		moves.sort(key=lambda x: x[0])  # sort by index of move
		move_indx, gap_len = moves[0]
		for i in range(file_len):
			disk[position + i] = None
			disk[move_indx + i] = fid_
		_ = heappop(gaps[gap_len])
		if gap_len > file_len:
			new_gap_len = gap_len - file_len
			new_gap_indx = move_indx + file_len
			heappush(gaps[new_gap_len], new_gap_indx)

print(chcksum(disk))
