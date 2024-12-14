__YEAR__ = 2023
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

import z3

import utils

# to run in Terminal: python3 src/python/main_py.py
# if output is to large: python3 src/python/main_py.py | less -R


class Solver:
    def __init__(self):
        pass

    def solve(self, testCase: int, input: str):
        lines = input.strip().split("\n")
        ans = 0
        x, y, z, vx, vy, vz = z3.Reals("x y z vx vy vz")
        solver = z3.Solver()
        for t, line in enumerate(lines):
            if t >= 3:
                break

            def parse(line):
                return [int(x) for x in re.findall(r"-?\d+", line)]
            x0, y0, z0, vx0, vy0, vz0 = parse(line)

            t = z3.Real(f"t_{t}")
            solver.add(x + vx * t == x0 + vx0 * t)
            solver.add(y + vy * t == y0 + vy0 * t)
            solver.add(z + vz * t == z0 + vz0 * t)

        assert (solver.check() == z3.sat)
        model = solver.model()

        x, y, z = model.eval(x), model.eval(
            y), model.eval(z)
        print("Coordinates: ", x, y, z)
        ans = model.eval(x + y + z)

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
