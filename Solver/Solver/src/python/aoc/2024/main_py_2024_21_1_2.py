__YEAR__ = 2024
__DAY__ = 21
# -----------------------------------------------------
from functools import cache
import math
import os

import copy
import queue
import collections

from pprint import pprint
from queue import Queue
from queue import PriorityQueue

from collections import deque
from collections import Counter
from collections import defaultdict

from sortedcontainers import SortedDict
from sortedcontainers import SortedSet
from sortedcontainers import SortedList
import heapq
import itertools
from functools import cmp_to_key

import sys
import fileinput
import re

import z3

import utils

# to run in Terminal: python3 src/python/main_py.py
# if output is to large: python3 src/python/main_py.py | less -R


def aoc_solver(testCase: int, input: str):
    lines = input.strip().split("\n")
    ans = 0
    # Solution is here

    num_pad = [
        ["7", "8", "9"],
        ["4", "5", "6"],
        ["1", "2", "3"],
        ["_", "0", "A"],
    ]

    dir_pad = [
        ["_", "^", "A"],
        ["<", "v", ">"],
    ]
    dir = {
        (0, -1): "<",
        (0, 1): ">",
        (-1, 0): "^",
        (1, 0): "v",
    }

    def get_ind(pad, ch):
        for i in range(len(pad)):
            for j in range(len(pad[0])):
                if pad[i][j] == ch:
                    return i, j

    def get_pad(type):
        if type == 0:
            return num_pad
        else:
            return dir_pad

    @cache
    def get_path(pad_type, seq, depth, next_seq):
        pad = get_pad(pad_type)
        if len(seq) == 1:
            if depth == 0:
                return len(next_seq)
            if pad_type != 0:  # direct tab
                sub = "A"
                sum = 0
                for i in range(len(next_seq)):
                    sub += next_seq[i]
                    if next_seq[i] == "A":
                        sum += get_path(1, sub, depth - 1, "")
                        sub = "A"
                return sum
            return get_path(1, "A" + next_seq, depth - 1, "")

        si, sj = get_ind(pad, seq[0])
        ni, nj = get_ind(pad, seq[1])
        di = ni - si
        if di != 0:
            di //= abs(di)
        dj = nj - sj
        if dj != 0:
            dj //= abs(dj)

        def move_horizontal():
            nonlocal sj
            r = ""
            while sj != nj:
                sj += dj
                if pad[si][sj] == "_":
                    sj -= dj
                    break
                r += dir[(0, dj)]
            return r

        def move_vertical():
            nonlocal si
            r = ""
            while si != ni:
                si += di
                if pad[si][sj] == "_":
                    si -= di
                    break
                r += dir[(di, 0)]
            return r

        def rest():
            r = ""
            if si != ni:
                r += move_vertical()
            if sj != nj:
                r += move_horizontal()
            return r + "A"

        if si == ni and sj == nj:
            return get_path(pad_type, seq[1:], depth, next_seq + "A")
        res_len = float("inf")
        _si, _sj = si, sj
        if sj != nj:
            res_len = get_path(pad_type, seq[1:], depth, next_seq + move_horizontal() + move_vertical() + rest())
        si, sj = _si, _sj
        if si != ni:
            res_len = min(get_path(pad_type, seq[1:], depth, next_seq + move_vertical() + move_horizontal() + rest()), res_len)
        return res_len

    ans = 0
    ans1 = 0
    for line in lines:
        r = get_path(0, "A" + line, 25, "")
        ans += r * int(line[:-1])
        r = get_path(0, "A" + line, 2, "")
        ans1 += r * int(line[:-1])
    print("Part 1: ", ans1)

    return ans


#  Test Cases -----------------------------------------------------------------------


def testCase(i, expected=None):
    utils.testCase(i, expected, lambda i, input: aoc_solver(i, input))


with open("src/output/output.txt", "w+") as file:
    sys.stdout = utils.writer(sys.stdout, file)

    testCase(1, 126384)
    # testCase(2)
    # testCase(3)
    # testCase(4)
    # testCase(5)

    utils.download_content(__YEAR__, __DAY__)
    testCase("puzzle")
