# words for writing practice - letters from some subset and length filter
c = 0
letters = set(list('клмнпстбвгджшх' + 'аоуыэиеё' + 'яю'))
for line in open('russian.txt').readlines():
    line = line.strip()
    if len(line) != 4:
        continue
    if set(list(line)) - letters:
        continue
    #if not set(list('яю')).intersection(set(list(line))):
    #    continue
    if not ('я' in line or 'ю' in line):
        continue
    print(line)
    c += 1

print(c)