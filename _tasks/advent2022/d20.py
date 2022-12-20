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

# a b C d
# a C b d

def move_left(i):
    b = l[i].prev
    d = l[i].next
    a = l[b].prev
    l[a].next = i
    l[i].prev = a
    l[i].next = b
    l[b].prev = i
    l[b].next = d
    l[d].prev = b

# a B c d
# a c B d
def move_right(i):
    a = l[i].prev
    c = l[i].next
    d = l[c].next
    l[a].next = c
    l[c].prev = a
    l[c].next = i
    l[i].prev = c
    l[i].next = d
    l[d].prev = i


def move(sign, i):
    if sign > 0:
        move_right(i)
    else:
        move_left(i)

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
    while v:
        v -= sign
        move(sign, i)


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
        while v:
            v -= sign
            move(sign, i)

a = get_next(1_000)
b = get_next(2_000)
c = get_next(3_000)
print(a, b, c)
print(a + b +c)
