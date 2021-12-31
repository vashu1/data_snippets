
def name_score(name):
    return sum([ord(c) + 1 - ord('a') for c in name.lower()])

assert name_score('COLIN') == 53

names = [name.replace('"', '').lower() for name in open('022.txt').readlines()[0].strip().split(',')]
names.sort()

res = 0
for indx, name in enumerate(names):
    assert name.isalpha()
    if name == 'colin':
        assert 938 == (indx+1)
    res += name_score(name) * (indx + 1)

print(res)