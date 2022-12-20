input_test = """1
2
-3
3
-2
0
4"""
input_test = input_test.split('\n')

input_full = open('d20.txt').readlines()

input = [l.strip() for l in input_full]

input = [int(i) for i in input]

l = input
avg = sum(l) / len(l)
print(f'{len(l)=} {len(set(l))=} {min(l)=} {max(l)=} {avg=} {len([i for i in l if i == 0])}')
# len(l)=5000 len(set(l))=3605 min(l)=-9998 max(l)=9987 avg=33.4942



# Part I


class R:
    def __init__(self, v):
        self.v = v


l = {i: R(c) for i, c in enumerate(input)}
zero = input.index(0)
for i in range(len(input)):
    l[i].next = (i + 1) % len(input)
    l[i].prev = (i - 1) % len(input)


# several times faster than single step move()
# 3m -> 30 sec
def move2(i, d):
    if d == 0:
        return
    a = l[i].prev
    b = l[i].next
    l[a].next = b
    l[b].prev = a
    if d > 0:
        while d > 1:
            b = l[b].next
            d -= 1
        a = b
        b = l[a].next
    else:
        while d < -1:
            a = l[a].prev
            d += 1
        b = a
        a = l[b].prev
    l[a].next = i
    l[b].prev = i
    l[i].prev = a
    l[i].next = b


def print_l():
    a = a_ = 0
    a = l[a].next
    s = ''
    while a != a_:
        s += f'{l[a].v} '
        a = l[a].next
    print(s)

for i in range(len(input)):
    #print(i)
    v = input[i]
    assert v == l[i].v
    sign = +1 if v > 0 else -1
    v = abs(v) % (len(input) - 1)
    v *= sign
    move2(i, v)


def get_next(n):
    a = zero
    while n:
        n -= 1
        a = l[a].next
    return l[a].v

a = get_next(1_000)
b = get_next(2_000)
c = get_next(3_000)
print(a, b, c)
print(a + b +c)
# 4139 101 2913
# 7153

# Part II

KEY = 811589153

l = {i: R(c * KEY) for i, c in enumerate(input)}

for i in range(len(input)):
    l[i].next = (i + 1) % len(input)
    l[i].prev = (i - 1) % len(input)


for turn in range(10):
    print(f'{turn=}')
    for i in range(len(input)):
        v = l[i].v
        sign = +1 if v > 0 else -1
        v = abs(v) % (len(input) - 1)
        v *= sign
        move2(i, v)

a = get_next(1_000)
b = get_next(2_000)
c = get_next(3_000)
print(a, b, c)
print(a + b +c)
