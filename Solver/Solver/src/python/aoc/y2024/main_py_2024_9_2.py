__YEAR__ = 2024
__DAY__ = 9
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
        lines = input.strip()

        ans = 0
        # Solution is here

        space = []
        size = [[] for x in range(10)]
        id = 0
        for i, p in enumerate(lines):
            if i % 2 == 0:
                for k in range(int(p)):
                    space.append(id)
                id += 1
            else:
                size[int(p)].append(len(space))
                for k in range(int(p)):
                    space.append(".")

        b_i = len(space) - 1

        def debug(space):
            l = [str(x) for x in space]
            print("".join(l))
        print(len(space))
        b_space = space.copy()
        while b_i > 0:
            while b_i > 0 and b_space[b_i] == ".":
                b_i -= 1

            right_bi = b_i
            while b_i > 0 and (b_space[b_i] != "." and b_space[b_i] == b_space[right_bi]):
                b_i -= 1

            if b_i > 0:
                block_size = right_bi - b_i

                def getMin():
                    min_ind = len(space)
                    min_i = 0
                    for i in range(block_size, 10):
                        if len(size[i]) > 0:
                            ind = size[i][0]
                            if ind > b_i:
                                continue
                            if min_ind > ind:
                                min_ind = ind
                                min_i = i
                    if min_ind == len(space):
                        return None
                    return (min_ind, min_i)

                if r := getMin():
                    min_ind, min_i = r
                    left_size = min_i - block_size
                    size[left_size].append(min_ind + block_size)
                    size[left_size].sort()
                    size[min_i].remove(min_ind)
                    for k in range(b_i + 1, right_bi + 1):
                        j = k - b_i - 1 + min_ind
                        space[j] = b_space[k]
                        space[k] = '.'

        # debug(space)

        for i in range(len(space)):
            if space[i] != '.':
                ans += space[i] * i

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
