input_test = """2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8"""
input_test = input_test.split('\n')

input_full = open('d04.txt').readlines()

# in how many assignment pairs does one range fully contain the other?

acc = 0
for line in [line.strip() for line in input_full]:  # input_full
    fst, snd = line.split(',')
    fst = fst.split('-')
    fst = list(map(int, fst))
    snd = snd.split('-')
    snd = list(map(int, snd))
    if fst[0] <= snd[0] and snd[1] <= fst[1]:
        #print(line)
        acc += 1
    elif snd[0] <= fst[0] and fst[1] <= snd[1]:
        #print(line)
        acc += 1

print(acc)

acc = 0
for line in [line.strip() for line in input_full]:  # input_full
    fst, snd = line.split(',')
    fst = fst.split('-')
    fst = list(map(int, fst))
    snd = snd.split('-')
    snd = list(map(int, snd))
    if fst[0] <= snd[0] and snd[1] <= fst[1]:
        print(line)
        acc += 1
    elif snd[0] <= fst[0] and fst[1] <= snd[1]:
        print(line)
        acc += 1
    elif fst[0] <= snd[0] <= fst[1]:
        acc += 1
    elif fst[0] <= snd[1] <= fst[1]:
        acc += 1
    elif snd[0] <= fst[0] <= snd[1]:
        acc += 1
    elif snd[0] <= fst[1] <= snd[1]:
        acc += 1

print(acc)