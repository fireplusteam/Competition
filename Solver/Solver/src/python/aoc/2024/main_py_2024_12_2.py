__YEAR__ = 2024
__DAY__ = 12
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
        field = input.strip().split("\n")
        ans = 0
        vis = set()
        # print(field)

        n = len(field)
        m = len(field[0])
        ans1 = 0
        for ii in range(n):
            for jj in range(m):
                area = 0
                fence = 0
                surround = set()

                def calc(ch, i, j):
                    nonlocal area, fence
                    key = (i, j)
                    if key in vis:
                        return
                    vis.add(key)
                    area += 1
                    d = [(0, 1), (0, -1), (1, 0), (-1, 0)]
                    for di, dj in d:
                        ni = i + di
                        nj = j + dj
                        if not (0 <= ni < n and 0 <= nj < m):
                            fence += 1
                            surround.add(
                                (ni * 4 - di, nj * 4 - dj, dj, di))
                            surround.add(
                                (ni * 4 - di, nj * 4 - dj, -dj, di))
                            continue
                        if field[ni][nj] == ch:
                            calc(ch, ni, nj)
                        else:
                            surround.add(
                                (ni * 4 - di, nj * 4 - dj, dj, di))
                            surround.add(
                                (ni * 4 - di, nj * 4 - dj, -dj, di))
                            fence += 1

                calc(field[ii][jj], ii, jj)
                v2 = set()
                r = 0
                for i, j, di, dj in surround:
                    if not (i, j, di, dj) in v2:
                        r += 1
                    else:
                        continue

                    while True:
                        i += di * 4
                        j += dj * 4

                        if not (i, j, di, dj) in surround:
                            break
                        v2.add((i, j, di, dj))
                        v2.add((i, j, -di, -dj))

                    while True:
                        i -= di * 4
                        j -= dj * 4
                        if not (i, j, di, dj) in surround:
                            break
                        v2.add((i, j, di, dj))
                        v2.add((i, j, -di, -dj))

                # if area > 0:
                #     print(area, r, ii, jj, field[ii][jj])
                ans += r * area
                ans1 += fence * area

        # Solution is here
        print("Part1:", ans1)

        return ans


#  Test Cases -----------------------------------------------------------------------

def testCase(i):
    solver = Solver()
    utils.testCase(i, lambda i, input: solver.solve(i, input))


testCase(1)
testCase(2)
testCase(3)
testCase(4)
testCase(5)


utils.download_content(__YEAR__, __DAY__)
testCase("puzzle")
