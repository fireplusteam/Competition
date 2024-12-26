__YEAR__ = 2024
__DAY__ = 15
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
        field, moves = input.strip().split("\n\n")
        moves = moves.replace("\n", "")
        field = [[x for x in y] for y in field.split("\n")]
        utils.debugPrint(field)
        print(moves)
        ans = 0
        # Solution is here
        dir = {
            ">": (0, 1),
            "<": (0, -1),
            "^": (-1, 0),
            "v": (1, 0)
        }
        n = len(field)
        m = len(field[0])

        def simulate(ri, rj):
            for step in moves:
                di, dj = dir[step]
                print("Step", step)

                path = [(ri, rj)]
                can_move = False
                ori, orj = ri, rj
                while True:
                    ni, nj = ri + di, rj + dj
                    if field[ni][nj] == '#':
                        break
                    elif field[ni][nj] == 'O':
                        path.append((ni, nj))
                    elif field[ni][nj] == '.':
                        path.append((ni, nj))
                        can_move = True
                        break
                    ri, rj = ni, nj
                if can_move:
                    path.reverse()
                    for i in range(1, len(path)):
                        i1, j1 = path[i - 1]
                        i2, j2 = path[i]
                        field[i1][j1], field[i2][j2] = field[i2][j2], field[i1][j1]
                    if len(path) >= 2:
                        ri, rj = path[-2]

                    print(ri, rj, path)
                    utils.debugPrint(field)
                else:
                    ri, rj = ori, orj

        for i in range(n):
            is_ = False
            for j in range(m):
                if field[i][j] == '@':
                    simulate(i, j)
                    is_ = True
                    break
            if is_:
                break
        for i in range(n):
            for j in range(m):
                if field[i][j] == 'O':
                    ans += 100 * i + j

        utils.debugPrint(field)

        return ans


#  Test Cases -----------------------------------------------------------------------

def testCase(i):
    solver = Solver()
    utils.testCase(i, lambda i, input: solver.solve(i, input))


with open("output.txt", "w+") as file:
    sys.stdout = file

    testCase(1)
    # testCase(2)
    # testCase(3)
    # testCase(4)
    # testCase(5)

    utils.download_content(__YEAR__, __DAY__)
    testCase("puzzle")
