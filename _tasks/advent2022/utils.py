"""
bisect
    from bisect import bisect_left
    indx = bisect_left(piles, elem)

intervals - pip install portion
    import portion as P
    >>> P.open(1, 2)
    (1,2)
    >>> P.open(1, 2).lower, P.open(1, 2).upper
    1, 2
    >>> P.closed(1, 2).left
    CLOSED
    >>> P.closed(1, 2)
    [1,2]
    >>> P.openclosed(1, 2)
    (1,2]
    >>> P.singleton(1)
    [1]
    >>> P.empty()
    ()
    i.intersection(other) and i & other return the intersection of two intervals.
    i.union(other) and i | other return the union of two intervals.
    i.complement(other) and ~i return the complement of the interval.
    i.difference(other) and i - other return the difference between i and other.
    >>> P.closed(0, 4) - P.closed(1, 2)
    [0,1) | (2,4]
    i.contains(other) and other in i hold if given item is contained in the interval. It supports intervals and arbitrary comparable values.
    i.adjacent(other) tests if the two intervals are adjacent, i.e., if they do not overlap and their union form a single atomic interval.
    i.overlaps(other) tests if there is an overlap between two intervals.
    ...
    >>> P.closed(0, 1) < P.closed(2, 3)
    True
    >>> P.closed(0, 1) < P.closed(1, 2)
    False

sortedcollections
    from sortedcontainers import SortedList, SortedSet, SortedDict
    sorted_list = SortedList([1, 3])
    sorted_list.add(2)  # [1,2,3]
    sorted_list.update([1,2])
    sorted_list.discard(8)  # only one
    sorted_list[1]
    ...
    sorted_set = SortedSet([1, 1, 2, 3, 4])
    sorted_set.add(i)
    sorted_set.discard(4)
    sorted_set[1]
    ...
    sorted_dict = SortedDict({'a': 1, 'b': 2, 'c': 3})
    sorted_dict.setdefault('e', 4)  # if does not exist

itertools
    itertools.permutations([v1,v2,v3])
    itertools.combinations([1,2,3], 3)])
    itertools.product(dog_types, repeat=8)
    def all_combinations(ps):
        return flatten(itertools.chain([itertools.combinations(ps,i) for i in range(1, len(ps))]))

collections
    d = deque('-')
    d.append('j')  # -j
    d.appendleft('f') # f-j
    d.pop() # j
    d.popleft() # f
    d.extend('jkl')
    d.rotate(1) # -1
    d.clear()

from heapq import heappush, heappop
    h = []
    heappush(h, value)
    heappop(h)
"""
import typing
import re


def flatten(lst):
    return [item for sublist in lst for item in sublist]


def lmap(func, *iterables):
    return list(map(func, *iterables))


def invert_dict(d):
    assert len(d) == len(set(d.values())), f'invert_dict() - we have repeating values!'
    return {v:k for k, v in d.items()}


def make_grid(*dimensions: typing.List[int], fill=0):  # make_grid(2,3) = [[0, 0, 0], [0, 0, 0]]
    if len(dimensions) == 1:
        return [fill for _ in range(dimensions[0])]
    next_down = make_grid(*dimensions[1:], fill=fill)
    return [list(next_down) for _ in range(dimensions[0])]


def add_border(lst, dims=None, fill=0):
    def _dims(lst):
        if not lst or not isinstance(lst, list):
            return []
        return [len(lst)] + _dims(lst[0])

    def _empty(dims, fill):
        if not dims:
            return fill
        return [_empty(dims[1:], fill) if dims[1:] else fill for _ in range(dims[0]+2)]
    if dims is None:
        dims = _dims(lst)
    if not dims:  # empty list, return element
        return lst
    return [_empty(dims[1:], fill)] +\
           [add_border(lst[j], dims[1:], fill) for j in range(dims[0])] +\
           [_empty(dims[1:], fill)]


def ints(s: str) -> typing.List[int]:
    return lmap(int, re.findall(r"-?\d+", s))


def floats(s: str) -> typing.List[float]:
    return lmap(float, re.findall(r"-?\d+(?:\.\d+)?", s))


def words(s: str) -> typing.List[str]:
    return re.findall(r"[a-zA-Z]+", s)


def list_diff(x):
    return [b-a for a, b in zip(x, x[1:])]


def get_rook_neighbours(height, width, row, col):
    res = []
    for i in [-1, 1]:
        if 0 <= col + i < width:
            res.append((row, col + i))
    for j in [-1, 1]:
        if 0 <= row + j < height:
            res.append((row+j, col))
    return res


def get_neighbours(height, width, row, col, dist):
    res = []
    for x in range(-dist, dist+1):
        for y in range(-dist, dist + 1):
            if x == 0 and y == 0:
                continue
            if 0 <= col + x < width and 0 <= row + y < height:
                res.append((row + y, col + x))
    return res


def print_grid(grid):
    for line in grid:
        print(*line, sep="")