__YEAR__ = 2020
__DAY__ = 24
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

import sys
import fileinput
import re

import utils

# to run in Terminal: python3 src/python/main_py.py
# if output is to large: python3 src/python/main_py.py | less -R


class Solver:
    def __init__(self):
        pass

    def solve(self, testCase: int, input: str):
        lines = input.strip().split("\n")
        ans = 0
        # Solution is here
        field = defaultdict(int)
        even = {
            "e": (0, 1),
            "se": (1, 0),
            "sw": (1, -1),
            "w": (0, -1),
            "nw": (-1, -1),
            "ne": (-1, 0)
        }

        odd = {
            "e": (0, 1),
            "se": (1, 1),
            "sw": (1, 0),
            "w": (0, -1),
            "nw": (-1, 0),
            "ne": (-1, 1)
        }

        def get_dir(i, j):
            if i % 2 == 0:
                return even
            return odd

        for line in lines:
            i, j = 0, 0
            k = 0
            while k < len(line):
                move = get_dir(i, j)
                if line[k] in move:
                    di, dj = move[line[k]]
                    i += di
                    j += dj
                    k += 1
                elif k + 1 < len(line) and line[k: k + 2] in move:
                    di, dj = move[line[k: k + 2]]
                    i += di
                    j += dj
                    k += 2
            if field[(i, j)] == 0:
                field[(i, j)] = 1
            else:
                field[(i, j)] = 0

        def count_ans():
            ans = 0
            for (_, _), val in field.items():
                ans += 1 if val == 1 else 0
            return ans
        print("Part 1: ", count_ans())

        def count_adj(i, j, color):
            res = 0
            for _, (di, dj) in get_dir(i, j).items():
                ni = i + di
                nj = j + dj
                cell_color = 1 if (
                    ni, nj) in field and field[(ni, nj)] == 1 else 0
                res += 1 if cell_color == color else 0
            return res

        for _ in range(100):
            next = {}
            for (i, j), val in field.items():
                if val == 1:  # black
                    adj_color = count_adj(i, j, 1)
                    if not (adj_color == 0 or adj_color > 2):
                        next[(i, j)] = 1

                    for _, (di, dj) in get_dir(i, j).items():
                        ni = i + di
                        nj = j + dj
                        if not (ni, nj) in field or field[(ni, nj)] == 0:
                            adj_color = count_adj(ni, nj, 1)
                            if adj_color == 2:
                                next[(ni, nj)] = 1

            field = next
            # print("Day ", step + 1, count_ans())

        ans = count_ans()

        return ans


#  Test Cases -----------------------------------------------------------------------

def testCase(i):
    solver = Solver()
    utils.testCase(i, lambda i, input: solver.solve(i, input))


testCase(1)
# testCase(2)
# testCase(3)
# testCase(4)
# testCase(5)


utils.download_content(__YEAR__, __DAY__)
testCase("puzzle")
