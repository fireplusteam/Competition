__YEAR__ = 2024
__DAY__ = 25
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

# to run in Terminal: python3 src/python/main_py.py
# if output is to large: python3 src/python/main_py.py | less -R


def aoc_solver(testCase: int, input: str):
    lines = input.strip().split("\n\n")
    ans = 0
    # Solution is here

    lock = []
    keys = []
    for field in lines:
        field = field.split("\n")
        n = len(field)
        m = len(field[0])

        def sum_row(i, ch):
            r = 0
            for j in range(m):
                r += field[i][j] == ch
            return r

        id = []
        for j in range(m):
            c = 0
            for i in range(1, n - 1):
                c += field[i][j] == "#"
            id.append(c)

        if sum_row(0, "#") == m:  # lock
            lock.append(id)
        else:
            keys.append(id)

    for l in lock:
        for k in keys:
            is_ = True
            for t1, t2 in zip(l, k):
                if t1 + t2 >= n - 1:
                    is_ = False

            ans += is_

    return ans


#  Test Cases -----------------------------------------------------------------------


def testCase(i, expected=None):
    utils.testCase(i, expected, lambda i, input: aoc_solver(i, input))


sys.setrecursionlimit(10**6)

with open("src/output/output.txt", "w+") as file:
    sys.stdout = utils.writer(sys.stdout, file)

    testCase(1, 3)
    # testCase(2)
    # testCase(3)
    # testCase(4)
    # testCase(5)

    utils.download_content(__YEAR__, __DAY__)
    testCase("puzzle")
