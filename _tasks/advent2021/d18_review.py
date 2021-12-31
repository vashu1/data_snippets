# advent of code day 18
# https://www.reddit.com/r/adventofcode/comments/rizw2c/2021_day_18_solutions/


import sys
import math
from functools import reduce

def parse_numbers(lines):
    for line in lines:
        it = iter(line)
        if next(it) != '[':
            raise ValueError
        yield parse_number_rec(it)

def parse_number_rec(it):
    c = next(it)
    if c == '[':
        left = parse_number_rec(it)
        c = next(it)
    else:
        left, c = parse_number_regular(c, it)
    if c != ',':
        raise ValueError
    c = next(it)
    if c == '[':
        right = parse_number_rec(it)
        c = next(it)
    else:
        right, c = parse_number_regular(c, it)
    if c != ']':
        raise ValueError
    return (left, right)

def parse_number_regular(c, it):
    n = 0
    while c in '0123456789':
        n *= 10
        n += int(c, 10)
        c = next(it)
    return n, c

def add_numbers(a, b):
    return reduce_number((a, b))

def reduce_number(n):
    reduced = True
    while reduced:
        n, reduced, *_ = explode_rec(n, 0)
        if not reduced:
            n, reduced = split_rec(n)
    return n

def explode_rec(n, level):
    if not isinstance(n, int):
        l, r = n
        if level >= 4:
            return 0, True, l, r
        else:
            l, reduced, expl, expr = explode_rec(l, level + 1)
            if reduced:
                if expr != 0:
                    r = add_left(r, expr)
                    expr = 0
            else:
                r, reduced, expl, expr = explode_rec(r, level + 1)
                if reduced:
                    if expl != 0:
                        l = add_right(l, expl)
                        expl = 0
            if reduced:
                return (l, r), True, expl, expr
    return n, False, 0, 0

def add_left(n, m):
    if isinstance(n, int):
        return n + m
    else:
        a, b = n
        return add_left(a, m), b

def add_right(n, m):
    if isinstance(n, int):
        return n + m
    else:
        a, b = n
        return a, add_right(b, m)

def split_rec(n):
    if isinstance(n, int):
        if n >= 10:
            a = n // 2
            return (a, n - a), True
    else:
        l, r = n
        l, reduced = split_rec(l)
        if not reduced:
            r, reduced = split_rec(r)
        if reduced:
            return (l, r), True
    return n, False

def number_magnitude(n):
    if isinstance(n, int):
        return n
    l, r = n
    return 3 * number_magnitude(l) + 2 * number_magnitude(r)

def part1(in_file):
    with open(in_file, 'r') as f:
        numbers = parse_numbers(map(str.strip, f))
        numbers = map(reduce_number, numbers)
        res = reduce(add_numbers, numbers)
    print(res)
    m = number_magnitude(res)
    print(m)

def part2(in_file):
    with open(in_file, 'r') as f:
        numbers = parse_numbers(map(str.strip, f))
        numbers = list(map(reduce_number, numbers))
    m_max = -math.inf
    for i, n1 in enumerate(numbers):
        for j, n2 in enumerate(numbers):
            if i == j: continue
            m = number_magnitude(add_numbers(n1, n2))
            if m > m_max:
                m_max = m
    print(m_max)

if __name__ == '__main__':
    part1(*sys.argv[1:])
    part2(*sys.argv[1:])










# UTILS
from typing import List


def add_to_rightmost_int(stack: List, x: int) -> List:
    """
    Add x to rightmost int in l
    if no int in l, do nothing
    return modified l
    """
    int_locations = [isinstance(i, int) for i in stack]
    if not any(int_locations):
        return stack
    int_locations.reverse()
    last_index = len(int_locations) - 1 - int_locations.index(True)
    stack[last_index] += x
    return stack


def add_to_leftmost_int(stack: List, x: int) -> List:
    """
    Add x to leftmost int in l
    if no int in l, do nothing
    return modified l
    """
    int_locations = [isinstance(i, int) for i in stack]
    if not any(int_locations):
        return stack
    index = int_locations.index(True)
    stack[index] += x
    return stack



from __future__ import annotations

import copy
import math
import os
import utils

from typing import List


class SFNumber:
    def __init__(self, snailfish_str: str) -> None:
        self.raw_number = copy.copy(snailfish_str)
        self._parse()

    def _parse(self):
        """ Convert string to internal format"""
        self.number = []
        current_digit = ""
        for char in self.raw_number:
            if char.isdigit():
                current_digit += char
            else:
                if current_digit != "":
                    self.number.append(int(current_digit))
                    current_digit = ""
                if char != ',':
                    self.number.append(char)

    def __repr__(self) -> str:
        return f"SFNumber({self.__str__()})"

    def __str__(self) -> str:
        output = ""
        for char in self.number:
            if output:
                if (output[-1] == ']' and char != ']'):
                    output += ','
                elif output[-1].isdigit() and char != ']':
                    output += ','
            output += str(char)
        return output

    def _explode_one(self) -> bool:
        stack = []
        index = 0
        depth = 0
        while index < len(self.number):
            x = self.number[index]
            if x == '[' and depth == 4:
                # EXPLOSTION DETECTED
                left_number = self.number[index + 1]
                right_number = self.number[index + 2]
                left_portion = utils.add_to_rightmost_int(stack, left_number)
                right_portion = utils.add_to_leftmost_int(
                    self.number[index + 4:], right_number
                )
                self.number = left_portion + [0] + right_portion
                return True
            else:
                if x == '[':
                    depth += 1
                elif x == ']':
                    depth -= 1
                stack.append(x)
            index += 1
        return False

    def _split_one(self) -> bool:
        stack = []
        index = 0
        while index < len(self.number):
            x = self.number[index]
            if isinstance(x, int) and x > 9:
                # SPLIT!
                left_number = math.floor(x/2)
                right_number = math.ceil(x/2)
                insert = ['[', left_number, right_number, ']']
                self.number = stack + insert + self.number[index + 1:]
                return True
            else:
                stack.append(x)
                index += 1
        return False

    def reduce(self) -> None:
        reduced = False
        while not reduced:
            if self._explode_one():
                continue
            if self._split_one():
                continue
            reduced = True

    def add(self, sf_number: SFNumber) -> None:
        new_number = ['[']
        new_number += self.number
        new_number += sf_number.number
        new_number += [']']
        self.number = new_number

    def _one_magnitude_layer(self, number):
        index = 0
        new_number = []
        while index < len(number):
            if number[index] == '[' and number[index + 3] == ']':
                left_number = number[index + 1] * 3
                right_number = number[index + 2] * 2
                new_number.append(left_number + right_number)
                index += 4
            else:
                new_number.append(number[index])
                index += 1
        return new_number

    @property
    def magnitude(self) -> int:
        magnitude = copy.copy(self.number)
        while len(magnitude) > 1:
            magnitude = self._one_magnitude_layer(magnitude)
        return magnitude.pop()


def process_snail_list(numbers: List[str]) -> SFNumber:
    result_number = None
    for number in numbers:
        new_number = SFNumber(number)
        if result_number is None:
            result_number = new_number
        else:
            result_number.add(new_number)
        result_number.reduce()
    return result_number


def parse_input_file(filename: str):
    current_dir = os.path.dirname(__file__)
    full_file_path = os.path.join(current_dir, filename)
    with open(full_file_path) as input_file:
        parsed_input = []
        for line in input_file.read().splitlines():
            parsed_input.append(line)
    return parsed_input


def find_largest_magnitude(number_list: List[str]):
    max_magnitude = 0
    for left_index in range(len(number_list)):
        for right_index in range(len(number_list)):
            if left_index != right_index:
                left_number = SFNumber(number_list[left_index])
                right_number = SFNumber(number_list[right_index])
                left_number.add(right_number)
                left_number.reduce()
                magnitude = left_number.magnitude
                if magnitude > max_magnitude:
                    max_magnitude = magnitude
    return max_magnitude


def main():
    parsed_input = parse_input_file("input.txt")
    snail_total = process_snail_list(parsed_input)

    part_1_result = snail_total.magnitude
    print(f"Part 1: {part_1_result}")

    part_2_result = find_largest_magnitude(parsed_input)
    print(f"Part 2: {part_2_result}")


if __name__ == "__main__":
    main()