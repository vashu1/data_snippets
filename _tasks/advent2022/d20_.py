from utils import *
from collections import defaultdict, Counter, deque
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



class Leave:
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

    def pop_leave(self, n):
        assert n == 0
        self.drop_parent()
        return self

    def add(self, leave, n):
        assert leave.parent is None
        assert self.parent
        assert n in [0, 1]
        self_parent = self.parent
        self.drop_parent()
        new_tree = Tree(leave, self) if n == 0 else Tree(self, leave)
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

    def pop_leave(self, n):
        assert 0 <= n < self.len
        self.len -= 1
        if self.len == 0:
            self.drop_parent()
        if self.left:
            if n < self.left.len:
                return self.left.pop_leave(n)
            else:
                n -= self.left.len
        assert 0 <= n < self.right.len
        return self.right.pop_leave(n)

    def add(self, leave, n):
        assert isinstance(leave, Leave)
        assert leave.parent is None
        assert 0 <= n <= self.len
        self.len += 1
        if self.left:
            if n < self.left.len or (n == self.left.len and random.random() < 0.5):
                self.left.add(leave, n)
                return
            else:
                n -= self.left.len
        elif n == 0:  # left is None
            self.left = leave
            leave.parent = self
            return
        if self.right:
            assert 0 <= n <= self.right.len
            self.right.add(leave, n)
            return
        elif n == 0:  # right is None
            self.right = leave
            leave.parent = self
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
        l = Leave(arr[0])
        r = Leave(arr[1]) if len(arr) == 2 else None
        positions.append(l)
        if r:
            positions.append(r)
        return Tree(l, r)
    half = len(arr) // 2
    l = tree_from_arr(arr[:half], positions)
    r = tree_from_arr(arr[half:], positions)
    return Tree(l, r)



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

def run_round():
    global tree
    c = 0
    for leave in positions_:
        #
        c += 1
        if c % 1_000_000 == 0:
            exit(0)  # TODO if needed
            print('rebuild tree')
            arr = tree.to_arr()
            tree = tree_from_arr(arr, positions_)  # need reorder leaves list
        assert tree.len == len(input)
        leave_index = leave.index()
        res = tree.pop_leave(leave_index)
        assert res == leave
        assert leave.parent is None
        assert tree.len == len(input) - 1
        assert isinstance(res, Leave) and res.len == 1 and res.value is not None and not isinstance(res.value, Tree)
        tree.add(leave, new_index(leave_index, leave.value))
        assert leave.parent

run_round()

# the grove coordinates can be found by looking at the 1000th, 2000th, and 3000th numbers after the value 0,
# wrapping around the list as necessary. In the above example, the 1000th number after 0 is 4, the 2000th is -3,
# and the 3000th is 2; adding these together produces 3.


arr = tree.to_arr()
index0 = arr.index(0)
a = arr[(index0 + 1_000) % len(arr)]
b = arr[(index0 + 2_000) % len(arr)]
c = arr[(index0 + 3_000) % len(arr)]
print(a, b, c)
print(a + b + c)

# PART II

KEY = 811589153

positions_ = []
tree = tree_from_arr([i * KEY for i in input], positions_)
for _ in range(10):
    run_round()

arr = tree.to_arr()
index0 = arr.index(0)
a = arr[(index0 + 1_000) % len(arr)]
b = arr[(index0 + 2_000) % len(arr)]
c = arr[(index0 + 3_000) % len(arr)]
print(a, b, c)
print(a + b + c)

"""


def flatten(lst):
    return [item for sublist in lst for item in sublist]


class Tree:
    def __init__(self, left, right=None, parent=None):
        if left is not None and not isinstance(left, Tree):
            assert right is None
        self.parent = parent
        self.len = 0
        self.left = left
        self.right = right
        if left is not None:
            self.len += left.len if isinstance(left, Tree) else 1
        if right is not None:
            self.len += right.len if isinstance(right, Tree) else 1
        if isinstance(left, Tree):
            left.connect(self)
        if isinstance(right, Tree):
            right.connect(self)

    def connect(self, new_parent):
        if self.parent is not None:
            if self.parent.left == self:
                self.parent.left = None
            elif self.parent.right == self:
                self.parent.right = None
            else:
                assert False
        assert new_parent is None or (new_parent.left == self or new_parent.right == self)
        self.parent = new_parent

    def __str__(self):
        return f'(Tree: {self.len})'

    def str(self):
        return f'({self.left} {self.right} {self.len=})'

    def consume_child(self, elem):
        print('consume_child')
        assert self.len == elem.len
        assert (self.left if self.left is not None else self.right) == elem
        elem.parent = None
        self.left = elem.left
        self.right = elem.right

    def drop_empty_childs(self):
        if isinstance(self.left, Tree):
            if self.left.len == 0:
                print('drop_empty_childs left disconnect')
                self.left.connect(None)
            elif self.left.len == self.len:
                print('---', self.str(), self.left.str(), self.right.str())
                assert self.right is None
                self.consume_child(self.left)
        if isinstance(self.right, Tree):
            if self.right.len == 0:
                print('drop_empty_childs right disconnect')
                self.right.connect(None)
            elif self.right.len == self.len:
                assert self.left is None
                self.consume_child(self.right)

    def pop_leave(self, n):
        print('pop', n)
        assert 0 <= n < self.len, f'{self.str()=} {n=}'
        # leave
        if self.left is not None and self.len == 1 and self.right is None and not isinstance(self.left, Tree):
            assert n == 0
            self.connect(None)
            return self
        self.len -= 1
        if self.left is not None:
            if n < self.left.len:
                v = self.left.pop_leave(n)
                self.drop_empty_childs()
                return v
            else:
                n -= self.left.len
        v = self.right.pop_leave(n)
        self.drop_empty_childs()
        return v

    def add(self, leave, n):
        print('add', self.len, n)
        assert n >= 0
        assert n <= self.len
        assert leave.len == 1

        # self is leave
        if self.left is not None and self.len == 1 and self.right is None and not isinstance(self.left, Tree):
            print('add', self.parent.str(), leave.str())
            assert n == 0 or n == 1
            assert self.parent.len > 1
            self_parent = self.parent
            if True:
                new_elem = Tree(leave, self) if n == 0 else Tree(self, leave)
                print('self_parent', self_parent.str())
                new_elem.parent = self_parent
                if self_parent.left is None:
                    self_parent.left = new_elem
                elif self_parent.right is None:
                    self_parent.right = new_elem
                else:
                    assert False
                tree.print()
            return
        #
        self.len += 1
        # is left a tree?
        if self.left is None and n == 0:
            self.left = leave
            leave.connect(self)
            return
        if self.left is not None:
            if n < self.left.len or (n == self.left.len and random.random() < 0.5):
                self.left.add(leave, n)
                return
            n -= self.left.len
        if self.right is None:
            assert n == 0
            self.right = leave
            leave.connect(self)
        else:
            self.right.add(leave, n)


    def index(self):
        if self.parent is None:
            return 0
        is_left = self.parent.left == self
        is_right = self.parent.right == self
        if is_left:
            return self.parent.index()
        elif is_right:
            res = self.parent.index()
            if isinstance(self.parent.left, Tree):
                res += self.parent.left.len
            return res
        else:
            assert False

    def to_arr(self, res=None):
        if res is None:
            res = []
        if self.left is not None:
            if isinstance(self.left, Tree):
                self.left.to_arr(res)
            else:
                res.append(self.left)
        if self.right is not None:
            if isinstance(self.right, Tree):
                self.right.to_arr(res)
            else:
                res.append(self.right)
        return res

    def print(self):
        level = 0
        stack = [self]
        while any(stack):
            print(level, '\t', '\t'.join([str(i) for i in stack]))
            new_stack = [([None, None] if i is None else ([i.left, i.right] if isinstance(i, Tree) else [None, None])) for i in stack]
            stack = flatten(new_stack)
            level += 1


def tree_from_arr(arr, positions):
    if len(arr) < 3:
        left = arr[0] if len(arr) > 0 else None
        left = None if left is None else Tree(left)
        if left is not None:
            positions.append(left)
        right = arr[1] if len(arr) > 1 else None
        right = None if right is None else Tree(right)
        if right is not None:
            positions.append(right)
        return Tree(left, right)
    else:
        half = len(arr) // 2
        left = tree_from_arr(arr[:half], positions)
        right = tree_from_arr(arr[half:], positions)
        return Tree(left, right)


"""