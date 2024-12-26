__YEAR__ = 2024
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
    ans = 0
    # Solution is here

    gr = defaultdict(set)
    for line in lines:
        a, b = line.split("-")
        gr[a].add(b)
        gr[b].add(a)
    r = set()
    for a in gr.keys():
        for b in gr[a]:
            for c in gr[b]:
                if a != b and b != c and a in gr[b] and a in gr[c] and b in gr[c] and (a.startswith("t") or b.startswith("t") or c.startswith("t")):
                    r.add(tuple(sorted([a, b, c])))
    ans = len(r)
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
