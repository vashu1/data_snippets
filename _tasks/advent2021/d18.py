import math
import copy

test = '''[1,2]
[[1,2],3]
[9,[8,7]]
[[1,9],[8,5]]
[[[[1,2],[3,4]],[[5,6],[7,8]]],9]
[[[9,[3,8]],[[0,9],6]],[[[3,7],[4,9]],3]]
[[[[1,3],[5,3]],[[1,3],[8,7]]],[[[4,9],[6,9]],[[8,2],[7,3]]]]'''

test2 = '''[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
[7,[5,[[3,8],[1,4]]]]
[[2,[2,2]],[8,[8,1]]]
[2,9]
[1,[[[9,3],9],[[9,0],[0,7]]]]
[[[5,[7,4]],7],1]
[[[[4,2],2],6],[8,7]]'''

test3='''[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]'''

input = '''[[[9,2],[[2,9],0]],[1,[[2,3],0]]]
[[[[2,0],2],[[6,4],[7,3]]],[0,[[3,0],[0,6]]]]
[[[[7,2],2],[9,[6,5]]],[[2,4],5]]
[[[[7,8],2],1],[[[5,4],[2,9]],[7,8]]]
[[[0,7],[1,[6,6]]],[[[0,7],9],4]]
[[[3,[9,6]],[5,1]],[[[0,1],6],[[7,6],0]]]
[[[3,0],[7,[4,0]]],[4,[[6,6],[5,3]]]]
[[[1,[4,8]],[2,[5,8]]],[[[3,6],[2,2]],[[3,8],[7,0]]]]
[9,[[[5,0],[0,3]],[2,[2,6]]]]
[[[3,[8,2]],[[8,0],5]],[[[7,6],[4,9]],[7,5]]]
[[7,[[4,1],9]],[5,1]]
[[[5,[7,5]],1],[8,[5,8]]]
[[[[0,2],7],[[1,4],[9,8]]],[[3,[0,3]],7]]
[[[[4,3],[7,4]],[6,[6,4]]],[8,0]]
[[[1,1],1],[[5,[2,7]],7]]
[[[5,4],5],[[7,[6,3]],[[8,4],6]]]
[[[7,9],[[4,4],[0,0]]],[[[8,6],6],[2,[6,4]]]]
[[[[4,7],[4,9]],3],[[[7,1],[8,6]],[9,[8,2]]]]
[6,[6,[2,9]]]
[[4,[[5,5],[5,0]]],[[[3,4],[9,5]],[8,6]]]
[2,[0,[2,5]]]
[[[4,[7,1]],[2,8]],[[7,0],[[1,6],1]]]
[[[3,4],[[7,8],[6,7]]],[[[6,2],[1,2]],5]]
[[[8,[0,8]],[[9,9],0]],[[[3,5],[4,2]],7]]
[[0,[[0,3],2]],[4,1]]
[[[[0,4],6],7],[[4,[9,1]],3]]
[[0,[[7,0],8]],[2,[8,[8,2]]]]
[[[[3,6],2],[9,4]],[6,[[7,9],[4,5]]]]
[[[[4,9],1],[[9,6],[8,8]]],[[7,[7,6]],[[8,3],[9,0]]]]
[2,0]
[[[[8,2],0],[3,5]],[[7,2],0]]
[[[[1,9],9],6],[9,[[9,3],[8,7]]]]
[[[9,[4,0]],[[7,1],[4,4]]],[[4,[2,3]],[8,7]]]
[[[[9,7],[5,6]],[4,[6,7]]],7]
[5,[[[8,2],8],[6,[7,9]]]]
[0,[[9,[0,1]],[[8,3],7]]]
[[[[4,5],[4,2]],[[5,2],[3,1]]],[[[3,1],[8,5]],8]]
[[0,4],[[2,[2,6]],[[1,1],3]]]
[[[0,8],[7,[5,8]]],7]
[[[7,2],[[6,6],[2,7]]],[[0,[9,3]],2]]
[[[[0,9],2],[[6,0],4]],3]
[[5,[[9,6],9]],[[6,[1,2]],[1,[6,2]]]]
[[[[3,9],5],[9,[7,2]]],[5,[[3,4],[0,6]]]]
[[2,[6,7]],[0,[[2,0],7]]]
[[2,[[5,4],[2,1]]],[2,[[8,7],[5,3]]]]
[[[[0,4],[2,5]],[1,2]],[5,[8,[0,3]]]]
[[[[9,2],[3,2]],[[2,9],4]],5]
[[[[8,9],5],1],[9,3]]
[[5,2],[3,[[8,5],2]]]
[[[0,1],[7,8]],[[[6,2],4],[[6,2],[9,5]]]]
[[[[9,6],5],2],2]
[[[[3,2],3],3],[[[0,1],1],[[8,4],8]]]
[[4,[2,[3,0]]],[[6,[7,0]],6]]
[[6,[[7,8],3]],[[[2,7],4],9]]
[0,2]
[[[9,1],[[3,7],[6,0]]],[[0,[4,1]],[[5,4],7]]]
[[[3,[9,4]],8],[[5,3],2]]
[[6,6],[[[0,5],[0,9]],[[5,5],4]]]
[[[[1,2],4],[[2,4],[8,0]]],[0,[[4,4],[5,8]]]]
[0,[[[9,0],3],[8,4]]]
[[4,5],[[[9,9],[3,5]],[8,[1,4]]]]
[[7,8],[[[3,1],[7,0]],[[4,7],[9,1]]]]
[[4,[2,[1,9]]],[[6,[6,1]],[[0,3],3]]]
[[[5,[0,9]],6],[[[3,4],[9,6]],[[4,0],[0,4]]]]
[[[1,5],[8,[2,8]]],[[5,[0,8]],[[0,7],[4,6]]]]
[[9,[0,2]],[[3,3],[3,1]]]
[[[[2,8],[5,9]],[2,[1,5]]],9]
[[3,[[8,9],[3,1]]],[[[9,0],7],[[0,4],3]]]
[[[[1,5],2],[5,[5,9]]],[5,[[0,1],[0,2]]]]
[6,[[[0,4],8],[[8,2],[5,5]]]]
[[[[7,7],5],[[8,2],7]],[2,5]]
[[[1,1],[[7,8],0]],3]
[[6,[[4,2],9]],[[[5,4],4],3]]
[[[[5,8],3],[[0,4],9]],[[[2,9],2],[3,4]]]
[[0,[4,8]],6]
[[[[9,5],[1,9]],[[3,7],[5,5]]],8]
[[1,9],6]
[[[4,[1,5]],3],0]
[[[2,[6,9]],5],[[5,7],[5,[7,1]]]]
[[[[3,1],[7,3]],[[1,0],[4,6]]],[[[4,9],[4,1]],[9,[2,0]]]]
[[[5,0],[[9,4],6]],[1,[[0,4],[9,9]]]]
[[[[9,8],3],[7,5]],[[[9,5],2],[9,9]]]
[[8,[[8,0],[2,3]]],[[[3,8],[2,6]],[[1,0],0]]]
[[[7,[7,1]],[[6,6],[2,9]]],[[5,[2,0]],[[3,9],[7,4]]]]
[1,[4,[[9,7],[1,3]]]]
[[0,3],[[[4,1],7],[[4,1],[3,0]]]]
[[0,[[7,7],6]],[[4,9],2]]
[[0,8],[4,[4,5]]]
[[[8,[0,5]],[[1,3],[0,5]]],[[2,6],[1,5]]]
[[[[7,6],8],[0,[2,7]]],8]
[8,[[[5,4],8],[[2,1],[7,5]]]]
[[[[7,3],[7,1]],0],[[[7,9],2],3]]
[[8,5],[6,6]]
[[[[5,2],8],7],[[[6,8],[1,0]],[[0,0],1]]]
[[[[1,0],1],6],[9,8]]
[[[[1,2],7],[1,[2,8]]],[[8,1],[[7,5],2]]]
[[0,6],[[2,8],[9,0]]]
[[[0,[7,7]],[2,[0,8]]],[[[7,4],4],[7,[4,0]]]]
[[[2,[9,3]],[[3,7],3]],[[[9,7],[5,6]],8]]
[[2,[[8,7],2]],[[8,[1,8]],[[7,2],1]]]'''

def reduce(data):
    path = find_explode(data)
    if path:
        old_val = get_v(data, path)
        a, b = old_val
        add(data, path, a)
        add(data, path, b, reverse_order=True)
        _ = assign(data, path, 0)
        return True
    else:
        return do_split(data)

def path_bigger(path, current_path, reverse_order):
    bigger = None
    for a, b in zip(path, current_path):
        if b>a:
            bigger = True
            break
        elif a>b:
            bigger = False
            break
    if reverse_order and bigger is not None:
        bigger = not bigger
    return bigger

def add(data, path, v, reverse_order=False, current_path=[]):
    if not current_path:
        current_path = []
    if path == current_path:
        return False
    i1, i2 = (0,1) if reverse_order else (1,0)
    if not path_bigger(path, current_path + [i1], reverse_order):
        if isinstance(data[i1], int):
            data[i1] += v
            return True
        else:
            if add(data[i1], path, v, reverse_order=reverse_order, current_path=current_path+[i1]):
                return True
    if not path_bigger(path, current_path + [i2], reverse_order):
        if isinstance(data[i2], int):
            data[i2] += v
            return True
        else:
            if add(data[i2], path, v, reverse_order=reverse_order, current_path=current_path+[i2]):
                return True
    return False


v = [[[[[9,8],1],2],3],4]
v2 = add(v, [0,0,0,0], 9)
print(v)
assert v2 == False
assert v == [[[[[9,8],1],2],3],4]
v = [7,[6,[5,[4,[3,2]]]]]
print('-----')
v2 = add(v, [1,1,1,1], 3)
assert v2 == True
print(v)
assert v == [7,[6,[5,[7,[3,2]]]]]
v = [7,[6,[5,[[3,2],4]]]]
v2 = add(v, [1,1,1,0], 3)
assert v2 == True
assert v == [7,[6,[8,[[3,2],4]]]]

v = [[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]
v2 = add(v, [0,1,1,1], 7)
assert v2 == True
assert [[3,[2,[8,[7,3]]]],[6,[5,[4,[3,2]]]]] == v
v2 = add(v, [0,1,1,1], 3, reverse_order=True)
assert v2 == True
assert [[3,[2,[8,[7,3]]]],[9,[5,[4,[3,2]]]]] == v

def get_v(data, path):
    for i in path:
        data = data[i]
    return data

def assign(data, path, val):
    for i in path[:-1]:
        data = data[i]
    saved = data[path[-1]]
    data[path[-1]] = val
    return saved

v = [1,[2,[3,4]]]
v2 = assign(v, [1, 1], 9)
assert v == [1,[2,9]]
assert v2 == [3,4]

def split(v):
    half = v / 2.0
    return [math.floor(half), math.ceil(half)]

assert split(10) == [5,5]
assert split(11) == [5,6]
assert split(12) == [6,6]

def do_split(data):
    assert isinstance(data, int) == False #if isinstance(data, int): return False
    l, r = data
    if isinstance(l, int):
        if l > 9:
            data[0] = split(l)
            return True
    else:
        if do_split(l):
            return True
    if isinstance(r, int):
        if r > 9:
            data[1] = split(r)
            return True
    else:
        if do_split(r):
            return True
    return False

v = [10,0]
do_split(v)
assert v == [[5,5],0]

def magnitude(data):
    l, r = data
    l = l if isinstance(l, int) else magnitude(l)
    r = r if isinstance(r, int) else magnitude(r)
    return 3*l + 2*r

assert magnitude([[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]) == 4140

def find_explode(data, path=[]):
    if not path:
        path = []  # to prevent overwrite of def param
    if isinstance(data, int):
        return None
    l, r = data
    if len(path) == 4:
        return path
    path.append(0)
    pl = find_explode(l, path=path)
    if pl:
        return pl
    _ = path.pop()
    path.append(1)
    pr = find_explode(r, path=path)
    if pr:
        return pr
    _ = path.pop()
    return None

assert find_explode([1,[2,3]]) is None
assert find_explode([[[[[9,8],1],2],3],4]) == [0,0,0,0]
assert find_explode([1,[[2,[3,[5,[7,8]]]],9]]) == [1,0,1,1]

v = [[[[[4,3],4],4],[7,[[8,4],9]]], [1,1]]
assert reduce(v)
assert [[[[0,7],4],[7,[[8,4],9]]],[1,1]] == v  # explode
assert reduce(v)
assert [[[[0,7],4],[15,[0,13]]],[1,1]] == v  # explode
assert reduce(v)
assert [[[[0,7],4],[[7,8],[0,13]]],[1,1]] == v  # split
assert reduce(v)
assert [[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]] == v  # split
assert reduce(v)
assert [[[[0,7],4],[[7,8],[6,0]]],[8,1]] == v  # explode
assert not reduce(v)
assert [[[[0,7],4],[[7,8],[6,0]]],[8,1]] == v  # nothing

print('\n\n\n===========\n\n\n')
v = [[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]], [7,[[[3,7],[4,3]],[[6,3],[8,8]]]]]
while reduce(v):
    print(v)
assert v == [[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]

data = [eval(l) for l in input.split('\n')]
res = data[0]

for i in data[1:]:
    res = [res, i]
    while reduce(res):
        pass
    print(res)

print(res)
print(magnitude(res))

data = [eval(l) for l in input.split('\n')]
v = []
for i in range(len(data)):
    for j in range(len(data)):
        if i != j:
            res = [copy.deepcopy(data[i]), copy.deepcopy(data[j])]
            while reduce(res):
                pass
            v.append(magnitude(res))

v.sort()
print(v)
print(max(v))


