__YEAR__ = 2024
__DAY__ = 18
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
    bb = [x.split(",") for x in lines]
    x = [int(x) for x, y in bb]
    y = [int(y) for x, y in bb]
    n = 70 + 1
    m = 70 + 1

    def simulate(end):
        field = utils.TwoD(n, m, 0)
        for i, (a, b) in enumerate(zip(x, y)):
            if i > end:
                break
            field[a][b] = 1

        q = queue.Queue()
        q.put((0, 0))
        dp = defaultdict(int)
        d = ((0, 1), (0, -1), (1, 0), (-1, 0))

        while not q.empty():
            i, j = q.get()
            cost = dp[(i, j)]
            # print(i, j, cost)

            for di, dj in d:
                ni, nj = i + di, j + dj
                if 0 <= ni < n and 0 <= nj < m and field[ni][nj] == 0:
                    if not (ni, nj) in dp:
                        dp[(ni, nj)] = cost + 1
                        q.put((ni, nj))
        return dp[(n - 1, m - 1)]

    l = 0
    r = len(x) - 1

    print("Part 1:", simulate(1023))

    while l <= r:
        mid = (l + r) // 2
        if simulate(mid) != 0:
            l = mid + 1
        else:
            ans = (x[mid], y[mid])
            r = mid - 1

    return ans


#  Test Cases -----------------------------------------------------------------------


def testCase(i, expected=None):
    utils.testCase(i, expected, lambda i, input: aoc_solver(i, input))


with open("src/output/output.txt", "w+") as file:
    sys.stdout = utils.writer(sys.stdout, file)

    # testCase(1)
    # testCase(2)
    # testCase(3)
    # testCase(4)
    # testCase(5)

    utils.download_content(__YEAR__, __DAY__)
    testCase("puzzle")
