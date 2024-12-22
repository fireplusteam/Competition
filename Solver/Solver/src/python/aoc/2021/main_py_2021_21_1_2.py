__YEAR__ = 2021
__DAY__ = 21
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

    lines = [int(x.replace("Player 1 starting position: ", "").replace("Player 2 starting position: ", "")) for x in lines]
    print(lines)

    def simulate(p1, p2):
        p1 = (p1 - 1) % 10
        p2 = (p2 - 1) % 10
        roll = 1
        score1 = 0
        score2 = 0
        while True:
            p1 = (p1 + roll + roll + 1 + roll + 2) % 10
            score1 += p1 + 1
            roll += 3
            if score1 >= 1000:
                break

            p2 = (p2 + roll + roll + 1 + roll + 2) % 10
            score2 += p2 + 1
            roll += 3
            if score2 >= 1000:
                break
        print(p1, p2, score1, score2, roll)
        return score2 * (roll - 1)

    @cache
    def rec(turn: int, p1: int, p2: int, score1: int, score2: int):
        # print(score1, score2)
        if score1 >= 21:
            return (1, 0)
        if score2 >= 21:
            return (0, 1)
        r1, r2 = 0, 0
        for roll1 in range(1, 4):
            for roll2 in range(1, 4):
                for roll3 in range(1, 4):
                    if turn == False:
                        np1 = (p1 + roll1 + roll2 + roll3) % 10
                        nscore1 = score1 + np1 + 1
                        a, b = rec(not turn, np1, p2, nscore1, score2)
                        r1 += a
                        r2 += b
                    else:
                        np2 = (p2 + roll1 + roll2 + roll3) % 10
                        nscore2 = score2 + np2 + 1
                        a, b = rec(not turn, p1, np2, score1, nscore2)
                        r1 += a
                        r2 += b
        return (r1, r2)

    print("Part 1: ", simulate(lines[0], lines[1]))
    ans = rec(False, (lines[0] - 1) % 10, (lines[1] - 1) % 10, 0, 0)

    return max(ans)


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
