
input = """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw"""
input = input.split('\n')

input = open('d03.txt').readlines()



def priority(v):
    if v.islower():
        return ord(v) - ord('a') + 1
    elif v.isupper():
        return 26 + priority(v.lower())
    else:
        assert False


input = [line.strip() for line in input]

acc = 0
for line in input:
    assert len(line) % 2 == 0
    fst = line[:len(line) // 2]
    snd = line[len(line) // 2:]
    for v in set(fst).intersection(set(snd)):
        acc += priority(v)
        #print(v, priority(v))

print(acc)

acc = 0
for indx in range(0, len(input), 3):
    for v in set(input[indx]).intersection(set(input[indx+1])).intersection(set(input[indx+2])):
        acc += priority(v)
        #print(v, priority(v))

print(acc)