__YEAR__ = 2022
__DAY__ = 13
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
    lines = input.strip().split("\n\n")
    ans = 0
    # Solution is here

    packets = []
    for ind, line in enumerate(lines):
        l1, l2 = line.split("\n")

        def parse(line, start):
            i = start
            res = []
            val = None
            while i < len(line):
                match line[i]:
                    case "[":
                        down, ni = parse(line, i + 1)
                        if start == 0:
                            res = down
                        else:
                            res.append(down)
                        i = ni + 1
                    case "]":
                        if val is not None:
                            res.append(val)
                        return res, i
                    case ",":
                        if val is not None:
                            res.append(val)
                        val = None
                        i += 1
                    case _:
                        if val is None:
                            val = 0
                        val = val * 10 + ord(line[i]) - ord("0")
                        i += 1
            if val is not None:
                res.append(val)
            return res

        def comp(l1, l2):
            if isinstance(l1, int) and isinstance(l2, int):
                return l1 - l2
            if not isinstance(l1, list):
                l1 = [l1]
            if not isinstance(l2, list):
                l2 = [l2]
            for a, b in zip(l1, l2):
                r = comp(a, b)
                if r == 0:
                    continue
                return r
            return len(l1) - len(l2)

        r1, r2 = parse(l1, 0), parse(l2, 0)
        assert (utils.print_to_string(r1).replace(" ", "") == l1)
        assert (utils.print_to_string(r2).replace(" ", "") == l2)
        packets += [r1, r2]
        # print(r1, r2)
        # print(comp(r1, r2), ind)
        ans += ind + 1 if comp(r1, r2) < 0 else 0
    print("Part 1:", ans)
    packets.append([[2]])
    packets.append([[6]])

    packets.sort(key=cmp_to_key(comp))

    i1 = packets.index([[2]]) + 1
    i2 = packets.index([[6]]) + 1
    ans = i1 * i2

    return ans


#  Test Cases -----------------------------------------------------------------------

def testCase(i):
    utils.testCase(i, lambda i, input: aoc_solver(i, input))


with open("src/output/output.txt", "w+") as file:
    sys.stdout = utils.writer(sys.stdout, file)

    testCase(1)
    # testCase(2)
    # testCase(3)
    # testCase(4)
    # testCase(5)

    utils.download_content(__YEAR__, __DAY__)
    testCase("puzzle")
