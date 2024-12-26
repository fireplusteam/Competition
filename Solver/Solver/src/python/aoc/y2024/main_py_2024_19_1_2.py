__YEAR__ = 2024
__DAY__ = 19
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
    towels, design = input.strip().split("\n\n")
    ans = 0
    # Solution is here

    towels = towels.split(", ")
    design = design.split("\n")

    ans1 = 0
    for d in design:
        assert len(d) > 0
        dp = defaultdict(int)
        dp[0] = 1
        for i in range(len(d)):
            for tow in towels:
                if d[i : i + len(tow)] == tow:
                    dp[i + len(tow)] += dp[i]
        ans += dp[len(d)]
        ans1 += dp[len(d)] > 0
    print("Part 1:", ans1)

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
