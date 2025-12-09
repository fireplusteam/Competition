__YEAR__ = 2025
__DAY__ = 9
__TASK_ID__ = ""  # used for tests input prefix like __TASK_ID__ = "A"
# -----------------------------------------------------
from functools import cache
import math
import cmath
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
import random

from sympy import isprime

import sys
import fileinput
import re

# third parties
# from z3 import z3
# import networkx

import utils
from utils import debugPrint
from utils import trace_recursive_calls

print = utils.printRec  # make recursive output with @trace_recursive_calls

# to run in Terminal: python3 src/python/solution.py < in.txt
# if output is to large: python3 src/python/solution.py < in.txt | less -R


def aoc_solver(testCase: int):
    input = sys.stdin.read().strip()
    # Input parser is here
    lines = input.split("\n")
    # print(lines)
    ans = 0
    n = len(lines)
    m = len(lines[0])
    print(n, m)
    points = []
    for line in lines:
        x, y = [int(x) for x in line.split(",")]
        points.append((x, y))

    def min(a, b):
        return a if a < b else b

    def max(a, b):
        return a if a > b else b

    def seg_inside(a, b, low, up):
        x1, y1 = a
        x2, y2 = b

        min_x, min_y = low
        max_x, max_y = up
        if min_x < x1 < max_x and min_y < y1 < max_y:
            return True
        if min_x < x2 < max_x and min_y < y2 < max_y:
            return True

        if x1 == x2 and min_x < x1 < max_x and max(y1, y2) >= max_y and min(y1, y2) <= min_y:
            return True
        if y1 == y2 and min_y < y1 < max_y and max(x1, x2) >= max_x and min(x1, x2) <= min_x:
            return True

        return False

    for i1 in range(len(points)):
        for i2 in range(i1 + 1, len(points)):
            x1, y1 = min(points[i1][0], points[i2][0]), min(points[i1][1], points[i2][1])
            x2, y2 = max(points[i1][0], points[i2][0]), max(points[i1][1], points[i2][1])
            valid = True
            for j in range(len(points)):
                if seg_inside(points[j], points[(j + 1) % len(points)], (x1, y1), (x2, y2)):
                    valid = False
                    break
            if valid:
                ans = max(ans, (x2 - x1 + 1) * (y2 - y1 + 1))
        # print(line)
    # Solution is here

    return ans


# run via terminal
if __name__ == "__main__":
    import time

    st = time.time()
    ans = aoc_solver(-1, input)
    print(f">  #Time = {time.time() - st: .5f}s")
    print(f">  {utils.Colors.WARNING}#Answer = {ans} {utils.Colors.ENDC}")
