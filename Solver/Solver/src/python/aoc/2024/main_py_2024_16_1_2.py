__YEAR__ = 2024
__DAY__ = 16
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

import z3

import utils

# to run in Terminal: python3 src/python/main_py.py
# if output is to large: python3 src/python/main_py.py | less -R


def aoc_solver(testCase: int, input: str):
    field = input.strip().split("\n")
    ans = 0
    # Solution is here

    pr = PriorityQueue()

    n = len(field)
    m = len(field[0])

    for i in range(n):
        for j in range(m):
            if field[i][j] == 'S':
                si, sj = i, j
                break

    d = ((0, 1), (-1, 0), (0, -1), (1, 0))

    pr.put((0, 0, si, sj))
    dp = defaultdict(lambda: float("inf"))
    dp[(0, si, sj)] = 0

    ans = 1e10
    q = queue.Queue()
    seen = set()

    while not pr.empty():
        cost, dir, i, j = pr.get()
        if field[i][j] == 'E':
            ans = cost
            q.put((dir, i, j))
            seen.add((dir, i, j))
            break
        di, dj = d[dir]

        for nd, ncost, (ni, nj) in [(dir, 1 + cost, (i + di, j + dj)), ((dir-1) % 4, 1000 + cost, (i, j)), ((dir + 1) % 4, 1000 + cost, (i, j))]:
            if not (0 <= ni < n and 0 <= nj < m) or field[ni][nj] == '#':
                continue
            key = (nd, ni, nj)
            if dp[key] > ncost:
                dp[key] = ncost
                pr.put((ncost, nd, ni, nj))

    print("Part 1: ", ans)
    while not q.empty():
        dir, i, j = q.get()
        di, dj = d[dir]
        for nd, ncost, (ni, nj) in [(dir, 1, (i - di, j - dj)), ((dir-1) % 4, 1000, (i, j)), ((dir + 1) % 4, 1000, (i, j))]:
            if (nd, ni, nj) in dp and dp[(dir, i, j)] == dp[(nd, ni, nj)] + ncost and not (nd, ni, nj) in seen:
                q.put((nd, ni, nj))
                seen.add((nd, ni, nj))
    grid_set = set()
    for (d, i, j) in seen:
        grid_set.add((i, j))
    ans = len(grid_set)

    return ans

    #  Test Cases -----------------------------------------------------------------------


def testCase(i):
    utils.testCase(i, lambda i, input: aoc_solver(i, input))


with open("src/output/output.txt", "w+") as file:
    sys.stdout = utils.writer(sys.stdout, file)

    testCase(1)
    testCase(2)
    # testCase(3)
    # testCase(4)
    # testCase(5)

    utils.download_content(__YEAR__, __DAY__)
    testCase("puzzle")
