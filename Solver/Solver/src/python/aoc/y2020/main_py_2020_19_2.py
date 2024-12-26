__YEAR__ = 2020
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

import sys
import fileinput
import re

import utils

# to run in Terminal: python3 src/python/main_py.py
# if output is to large: python3 src/python/main_py.py | less -R


class Solver:
    def __init__(self):
        pass

    def solve(self, testCase: int, input: str):
        rules, strings = input.strip().split("\n\n")

        gr = defaultdict(list[str])
        for i in rules.split("\n"):
            i = re.split(": | ", i)
            rule = i[0]
            l = []
            for j in i[1:]:
                if j == "|":
                    gr[rule].append(l)
                    l = []
                else:
                    l.append(j.strip("\""))
            gr[rule].append(l)

        ans = 0
        # Solution is here
        # part 2: the only difference of those two lines
        gr["8"] = [["42"], ["42", "8"]]
        gr["11"] = [["42", "31"], ["42", "11", "31"]]

        for q in strings.split("\n"):
            @cache
            def check(q, rule):
                if rule == q:
                    return True

                for i in gr[rule]:
                    if len(i) == 1:
                        if check(q, i[0]):
                            return True
                    elif len(i) == 2:
                        for k1 in range(1, len(q)):
                            if check(q[:k1], i[0]) and check(q[k1:], i[1]):
                                return True
                    elif len(i) == 3:
                        for k1 in range(1, len(q)):
                            for k2 in range(k1 + 1, len(q)):
                                if (check(q[:k1], i[0]) and check(q[k1:k2], i[1]) and check(q[k2:], i[2])):
                                    return True
                return False

            res = check(q, "0")
            ans += 1 if res else 0

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
