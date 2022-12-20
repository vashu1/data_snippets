from utils import *
import random

input_test = """1
2
-3
3
-2
0
4"""
input_test = input_test.split('\n')

input_full = open('d20.txt').readlines()

input = [l.strip() for l in input_test]
l = [int(i) for i in input]
input = l
avg = sum(l) / len(l)
print(f'{len(l)=} {len(set(l))=} {min(l)=} {max(l)=} {avg=} {len([i for i in l if i == 0])}')
# len(l)=5000 len(set(l))=3605 min(l)=-9998 max(l)=9987 avg=33.4942



class Leaf:
    def __init__(self, value):
        assert value is not None
        self.value = value
        self.len = 1
        self.parent = None

    def to_arr(self, res):
        res.append(self.value)

    def drop_parent(self):
        assert self.parent
        if self.parent.left == self:
            self.parent.left = None
        elif self.parent.right == self:
            self.parent.right = None
        else:
            assert False
        self.parent = None

    def pop_leaf(self, n):
        assert n == 0
        self.drop_parent()
        return self

    def add(self, leaf, n):
        assert leaf.parent is None
        assert self.parent
        assert n in [0, 1]
        self_parent = self.parent
        self.drop_parent()
        new_tree = Tree(leaf, self) if n == 0 else Tree(self, leaf)
        new_tree.parent = self_parent
        if self_parent.left is None:
            self_parent.left = new_tree
        elif self_parent.right is None:
            self_parent.right = new_tree
        else:
            assert False

    def index(self):
        assert self.parent
        res = self.parent.index()
        if self.parent.right == self:
            if self.parent.left:
                res += self.parent.left.len
        return res

    def print(self, level):
        print('\t' * level, self.value)

    def get_depth(self):
        return 1


class Tree:
    def __init__(self, left, right=None):
        self.parent = None
        self.len = 0
        self.left = left
        self.right = right
        if left is not None:
            self.len += left.len
            left.parent = self
        if right is not None:
            self.len += right.len
            right.parent = self

    def drop_parent(self):
        if self.parent:
            if self.parent.left == self:
                self.parent.left = None
            elif self.parent.right == self:
                self.parent.right = None
            else:
                assert False
        self.parent = None

    def pop_leaf(self, n):
        assert 0 <= n < self.len
        self.len -= 1
        if self.len == 0:
            self.drop_parent()
        if self.left:
            if n < self.left.len:
                return self.left.pop_leaf(n)
            else:
                n -= self.left.len
        assert 0 <= n < self.right.len
        return self.right.pop_leaf(n)

    def add(self, leaf, n):
        assert isinstance(leaf, Leaf)
        assert leaf.parent is None
        assert 0 <= n <= self.len
        self.len += 1
        if self.left:
            if n < self.left.len or (n == self.left.len and random.random() < 0.5):
                self.left.add(leaf, n)
                return
            else:
                n -= self.left.len
        elif n == 0:  # left is None
            self.left = leaf
            leaf.parent = self
            return
        if self.right:
            assert 0 <= n <= self.right.len
            self.right.add(leaf, n)
            return
        elif n == 0:  # right is None
            self.right = leaf
            leaf.parent = self
            return
        assert False

    def index(self):
        if self.parent is None:
            return 0
        is_left = self.parent.left == self
        is_right = self.parent.right == self
        assert is_left or is_right
        assert not (is_left and is_right)
        if is_left:
            return self.parent.index()
        elif is_right:
            res = self.parent.index()
            if self.parent.left:
                res += self.parent.left.len
            return res
        else:
            assert False

    def to_arr(self, res=None):
        if res is None:
            res = []
        if self.left is not None:
            self.left.to_arr(res)
        if self.right is not None:
            self.right.to_arr(res)
        return res

    def get_depth(self):
        l = r = -1
        if self.left:
            l = self.left.get_depth()
        if self.right:
            r = self.right.get_depth()
        return max(l + 1, r + 1)

    def print(self, level=0):
        print('\t' * level, f'{self.len=}')
        if self.left:
            self.left.print(level+1)
        if self.right:
            self.right.print(level+1)


def tree_from_arr(arr, positions):
    if len(arr) == 0:
        return None
    if len(arr) in [1, 2]:
        l = Leaf(arr[0])
        r = Leaf(arr[1]) if len(arr) == 2 else None
        positions.append(l)
        if r:
            positions.append(r)
        return Tree(l, r)
    half = len(arr) // 2
    l = tree_from_arr(arr[:half], positions)
    r = tree_from_arr(arr[half:], positions)
    return Tree(l, r)

def rebuild_tree(positions):
    tree = tree_from_arr(positions, [])  # need to reorder leaves list
    stack = [tree]
    while stack:
        v = stack.pop()
        if isinstance(v.left, Tree):
            stack.append(v.left)
        if isinstance(v.right, Tree):
            stack.append(v.right)
        if isinstance(v.left, Leaf):
            assert isinstance(v.left.value, Leaf)
            v.left = v.left.value
            v.left.parent = v
        if isinstance(v.right, Leaf):
            assert isinstance(v.right.value, Leaf)
            v.right = v.right.value
            v.right.parent = v
    return tree


positions_ = []
tree = tree_from_arr(input, positions_)

# check
assert len(positions_) == len(input)
for i, v in enumerate(positions_):
    assert v.value == input[i]
    assert v.index() == i

def new_index(index, delta):
    result = index + delta
    result = result % (len(input) - 1)
    return result

max_depth = 0
def run_round():
    global tree, max_depth
    c = 0
    for leaf in positions_:
        if tree.get_depth() > max_depth:
            max_depth = tree.get_depth()
            print(f'{max_depth=}')
        #
        c += 1
        if max_depth > 20:
            max_depth = 0
            print('rebuild tree')
            tree = rebuild_tree(positions_)
        assert tree.len == len(input)
        leaf_index = leaf.index()
        res = tree.pop_leaf(leaf_index)
        assert res == leaf
        assert leaf.parent is None
        assert tree.len == len(input) - 1
        assert isinstance(res, Leaf) and res.len == 1 and res.value is not None and not isinstance(res.value, Tree)
        tree.add(leaf, new_index(leaf_index, leaf.value))
        assert leaf.parent

run_round()

# the grove coordinates can be found by looking at the 1000th, 2000th, and 3000th numbers after the value 0,
# wrapping around the list as necessary. In the above example, the 1000th number after 0 is 4, the 2000th is -3,
# and the 3000th is 2; adding these together produces 3.

def print_result():
    arr = tree.to_arr()
    index0 = arr.index(0)
    a = arr[(index0 + 1_000) % len(arr)]
    b = arr[(index0 + 2_000) % len(arr)]
    c = arr[(index0 + 3_000) % len(arr)]
    print(a, b, c)
    print(a + b + c)

print_result()

# PART II

KEY = 811589153

positions_ = []
tree = tree_from_arr([i * KEY for i in input], positions_)
for _ in range(10):
    run_round()

print_result()