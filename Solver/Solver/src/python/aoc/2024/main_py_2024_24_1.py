__YEAR__ = 2024
__DAY__ = 24
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
# import z3
# import networkx

import utils
from utils import printRec
from utils import debugPrint
from utils import trace_recursive_calls

# to run in Terminal: python3 src/python/main_py.py
# if output is to large: python3 src/python/main_py.py | less -R


def aoc_solver(testCase: int, input: str):
    wire, gates = input.strip().split("\n\n")
    ans = 0
    # Solution is here

    gr_w = {}
    for w in wire.split("\n"):
        name, value = w.split(": ")
        gr_w[name] = int(value)
    print(gr_w)

    gr_g = {}
    dest = set()
    for g in gates.split("\n"):
        command, out = g.split(" -> ")
        a, com, b = command.split(" ")
        gr_g[out] = (a, com, b)
        if out.startswith("z"):
            dest.add(out)
    print(gr_g)
    dest = sorted(list(dest))
    print(dest)

    for s, i in enumerate(dest):

        def com_res(a, com, b):
            match com:
                case "AND":
                    return a & b
                case "OR":
                    return a | b
                case "XOR":
                    return a ^ b
            assert False

        # @trace_recursive_calls()
        @cache
        def dfs(v):
            if v in gr_g:
                a, com, b = gr_g[v]
                a = dfs(a)
                b = dfs(b)
                return com_res(a, com, b)
            if v in gr_w:
                return gr_w[v]
            assert False

        ans = ans + dfs(i) * 2**s

    return ans


#  Test Cases -----------------------------------------------------------------------


def testCase(i, expected=None):
    utils.testCase(i, expected, lambda i, input: aoc_solver(i, input))


sys.setrecursionlimit(10**6)

with open("src/output/output.txt", "w+") as file:
    sys.stdout = utils.writer(sys.stdout, file)

    testCase(1, 4)
    testCase(2, 2024)
    # testCase(3)
    # testCase(4)
    # testCase(5)

    utils.download_content(__YEAR__, __DAY__)
    testCase("puzzle")
