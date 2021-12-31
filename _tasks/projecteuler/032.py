
o32 = __import__("024")

input = '123456789'

def check(lst):
    s = ''.join(lst)
    res = []
    for l1 in range(1, 6+1):
        for l2 in range(l1+1, 9):
            i1 = int(s[:l1])
            i2 = int(s[l1:l2])
            i3 = int(s[l2:])
            if i1*i2 == i3:
                res.append((i1,i2,i3))
    return res

perm = list(input)
c = 0
res = check(perm)
while perm != list('987654321'):
    if c%1000 == 0:
        print(c)
    o32.next_perm(perm)
    res += check(perm)
    c += 1

print(c)
print(res)
# HINT: Some products can be obtained in more than one way so be sure to only include it once in your sum.
print(sum(set([v[2] for v in res])))