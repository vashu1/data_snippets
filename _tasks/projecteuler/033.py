


for a in range(10, 100):
    for b in range(a, 100):
        v1 = a / b
        if v1 >= 1:
            continue
        if b % 10 == 0:
            continue
        v2 = (a//10) / (b//10)
        if v1 == v2:
            print(f'a/b = {a} / {b}   {v1=} {v2=}')

#