__YEAR__ = 2020
__DAY__ = 21
# -----------------------------------------------------
import math
import os

import copy
import queue
import collections

from pprint import pprint
from queue import Queue
from queue import PriorityQueue

from collections import deque
from collections import OrderedDict
from collections import Counter
from collections import defaultdict

from sortedcontainers import SortedDict
from sortedcontainers import SortedSet
from sortedcontainers import SortedList

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
        lines = input.strip().split("\n")
        ans = 0
        # Solution is here

        print((set(["1", "2"]) - set(["1"])))

        data = []
        all_alerg = set()
        all_ing = set()
        for line in lines:
            ing_line, alerg_line = line.split(" (contains ")
            alerg_line = alerg_line.replace(")", "")
            ing = set(list(ing_line.split(" ")))
            alerg = set(alerg_line.split(", "))
            data.append((ing, alerg))
            all_alerg |= alerg
            all_ing |= ing

        utils.debugPrint(data)

        removed_ing = set()
        data_copy = copy.deepcopy(data)
        while True:
            is_reduced = False
            next_data = copy.deepcopy(data)
            for i, a in data:
                if len(i) == len(a):  # remove
                    for _i, _a in next_data:
                        c = len(_i)
                        _i -= i
                        if len(_i) != c:
                            is_reduced = True
                        c = len(_a)
                        _a -= a
                        if len(_a) != c:
                            is_reduced = True
            next_data = list(filter(lambda a: len(
                a[0]) > 0 and len(a[1]) > 0, next_data))
            data = next_data

            for ing in all_ing:
                can_be_deleted = True
                for match_alerg in all_alerg:
                    def is_valid_match():
                        for i, a in data:
                            if match_alerg in a and not ing in i:
                                return False
                        return True
                    if is_valid_match():  # remove
                        can_be_deleted = False
                        break
                if can_be_deleted:
                    removed_ing.add(ing)
                    # print(ing, match_alerg)
                    for _i, _a in data:
                        c = len(_i)
                        _i -= set([ing])
                        if c != len(_i):
                            is_reduced = True
            # print(data)
            if not is_reduced:
                break
        for (i, a) in data_copy:
            for j in i:
                ans += 1 if j in removed_ing else 0
        print("-----------")
        utils.debugPrint(data)
        print(removed_ing)
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
