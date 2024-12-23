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
    r = [{x} for x in gr.keys()]

    ans = 0
    v_set = set()
    for _ in range(len(gr)):
        next = set()
        for connected in r:
            intersected = gr.keys() - connected
            for a in connected:
                intersected &= gr[a]
                if len(intersected) == 0:
                    break

            for d in intersected:

                def is_connected_to_d():
                    for v in connected:
                        if v not in gr[d]:
                            return False
                    return True

                if is_connected_to_d():
                    key = list(connected)

                    key.append(d)
                    key.sort()
                    if len(key) > ans:
                        v_set = key
                        ans = len(key)
                    next.add(tuple(key))
        r = next
        if len(r) == 0:
            break

    return ",".join(sorted(list(v_set)))


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
