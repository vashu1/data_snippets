input_test = """    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2"""
input_test = input_test.split('\n')

input_full = open('d05.txt').readlines()


input = input_full
# parse
empty_index = 0
while input[empty_index].strip():
    empty_index += 1

stacks = input[empty_index-1]
stacks = [i for i in stacks.split(' ') if i]
stacks = [list() for i in range(len(stacks))]
for i in range(empty_index-2, 0-1, -1):
    line = [input[i][j] for j in range(1, len(input[i]), 4)]
    for indx, k in enumerate(line):
        if k != ' ':
            stacks[indx].append(k)

#print(stacks)
for indx in range(empty_index+1, len(input)):  # move 6 from 4 to 3
    if not input[indx].strip():
        continue
    #print(input[indx].strip().split(' '))
    _, cnt, _, from_, _, to_ = input[indx].strip().split(' ')
    cnt = int(cnt)
    from_ = int(from_) - 1
    to_ = int(to_) - 1
    #print(stacks)
    #for k in range(cnt):  # 1st part
    #    stacks[to_].append(stacks[from_].pop())
        #print(stacks)
    stacks[to_] += stacks[from_][-cnt:]  # 2nd part
    stacks[from_] = stacks[from_][:-cnt]

print(''.join([lst[-1] if lst else '' for lst in stacks]))
