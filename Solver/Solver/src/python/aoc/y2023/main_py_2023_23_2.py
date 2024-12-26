__YEAR__ = 2023
__DAY__ = 23
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


class Solver:
    def __init__(self):
        pass

    def solve(self, testCase: int, input: str):
        field = input.strip().split("\n")
        field = [[x if x == '#' else '.' for x in y] for y in field]
        d = ((-1, 0), (1, 0), (0, -1), (0, 1))

        gr = defaultdict(list)
        n = len(field)
        m = len(field[0])
        for i, line in enumerate(field):
            for j, ch in enumerate(line):
                if ch == '.':
                    for di, dj in d:
                        ni, nj = i + di, j + dj
                        if ni in range(n) and nj in range(m) and field[ni][nj] == '.':
                            gr[(i, j)].append((ni, nj))
        # compress
        source_i, source_j = 0, 1
        dest_i, dest_j = n - 1, m - 2

        def compress(gr: defaultdict[list]):
            cm_gr = defaultdict(list)
            for (ui, uj), adj in gr.items():
                seen = set()

                def check_if_not_compressed(ui, uj, adj):
                    return len(adj) > 2 or (ui, uj) == (source_i, source_j) or (ui, uj) == (dest_i, dest_j)
                if (check_if_not_compressed(ui, uj, adj)):
                    q = queue.Queue()
                    seen |= {(ui, uj)}
                    for (vi, vj) in adj:
                        seen |= {(vi, vj)}
                        q.put((vi, vj, 1))

                    while not q.empty():
                        i, j, cost = q.get()
                        if check_if_not_compressed(i, j, gr[(i, j)]):
                            cm_gr[(ui, uj)].append((i, j, cost))
                            continue
                        for (vi, vj) in gr[(i, j)]:
                            if not (vi, vj) in seen:
                                seen |= {(vi, vj)}
                                q.put((vi, vj, cost + 1))
            return cm_gr

        best_known = 0

        def find_longest(gr, ui, uj, cost, seen):
            nonlocal best_known
            if best_known < cost and ui == dest_i and uj == dest_j:
                best_known = cost
                print(best_known)
            adj = gr[(ui, uj)]
            for (vi, vj, edg_cost) in adj:
                if not (vi, vj) in seen:
                    seen.add((vi, vj))
                    find_longest(gr, vi, vj, cost + edg_cost, seen)
                    seen.remove((vi, vj))

        gr = compress(gr)
        find_longest(gr, source_i, source_j, 0, set([(source_i, source_j)]))
        ans = best_known

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
