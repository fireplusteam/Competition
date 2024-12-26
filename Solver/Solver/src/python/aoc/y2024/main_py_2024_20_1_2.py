__YEAR__ = 2024
__DAY__ = 20
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
    field = input.strip().split("\n")
    field = [[x for x in y] for y in field]
    ans = 0
    n = len(field)
    m = len(field[0])
    for i in range(n):
        for j in range(m):
            if field[i][j] == "S":
                si, sj = i, j
                field[i][j] = "."
            if field[i][j] == "E":
                ei, ej = i, j
                field[i][j] = "."

    dir = ((0, 1), (0, -1), (-1, 0), (1, 0))

    def bfs(field):
        q = Queue()
        q.put((si, sj, 0))
        dp = {}
        dp[(si, sj)] = 0

        while not q.empty():
            i, j, cost = q.get()
            if i == ei and j == ej:
                return cost, dp

            def add(ni, nj):
                if (ni, nj) in dp:
                    return
                if field[ni][nj] == "#":
                    return
                q.put((ni, nj, cost + 1))
                dp[(ni, nj)] = cost + 1

            for di, dj in dir:
                ni, nj = i + di, j + dj
                if 0 <= ni < n and 0 <= nj < m:
                    add(ni, nj)

    cost, dp = bfs(field)

    def calc_all_pairs(end):
        ans = 0
        for i in range(n):
            for j in range(m):
                if not (i, j) in dp:
                    continue
                for ni in range(i - end, i + end + 1):
                    for nj in range(j - end, j + end + 1):
                        cheat_dist = abs(i - ni) + abs(j - nj)
                        if cheat_dist <= end:
                            if (ni, nj) in dp:
                                dist = cost - dp[(ni, nj)] + dp[(i, j)] + cheat_dist
                                if 100 <= cost - dist:
                                    ans += 1
        return ans

    print("Part 1:", calc_all_pairs(2))
    ans = calc_all_pairs(20)

    return ans


#  Test Cases -----------------------------------------------------------------------


def testCase(i, expected=None):
    utils.testCase(i, expected, lambda i, input: aoc_solver(i, input))


with open("src/output/output.txt", "w+") as file:
    sys.stdout = utils.writer(sys.stdout, file)

    testCase(1)
    # testCase(2)
    # testCase(3)
    # testCase(4)
    # testCase(5)

    utils.download_content(__YEAR__, __DAY__)
    testCase("puzzle")
