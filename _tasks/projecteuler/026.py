# 1/7	= 	0.(142857)

def calc(n):
    divs = [0]
    mods = [10]
    while True:
        v = mods[-1]*10
        divs.append(v // n)
        mods.append(v % n)
        # check cycle
        for i in range(2, len(divs) // 2 + 1):
            if divs[-1] == divs[-i] and mods[-1] == mods[-i]:
                print(n, '0.' + ''.join([str(d) for d in divs[1:]]))
                return i - 1

vals = {n: calc(n) for n in range(1, 1000)}
m = max(vals.values())
for n in vals:
    if vals[n] == m:
        print(n, vals[n])