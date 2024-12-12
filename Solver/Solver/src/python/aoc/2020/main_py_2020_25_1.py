__YEAR__ = 2020
__DAY__ = 25
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
        lines = input.strip().split("\n")
        card_public = int(lines[0])
        door_public = int(lines[1])

        def calc(loop_size, subject_number=7):
            val = 1
            for _ in range(loop_size):
                val *= subject_number
                val %= 20201227
            return val

        def find_loop_num(target):
            ind = 1
            val = 1
            while True:
                val *= 7
                val %= 20201227
                if val == target:
                    return ind
                ind += 1

        loop_size_card = find_loop_num(card_public)
        loop_size_door = find_loop_num(door_public)
        print(loop_size_card)
        print(loop_size_door)

        ans = calc(loop_size_card, door_public)
        assert (ans == (calc(loop_size_door, card_public)))

        # Solution is here

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
