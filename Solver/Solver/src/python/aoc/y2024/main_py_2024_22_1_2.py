__YEAR__ = 2024
__DAY__ = 22
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
import cmath

# to run in Terminal: python3 src/python/main_py.py
# if output is to large: python3 src/python/main_py.py | less -R


def aoc_solver(testCase: int, input: str):
    lines = input.strip().split("\n")
    ans = 0
    # Solution is here
    modulo = 16777216

    def gen_secret(secret_num):
        secret_num ^= secret_num * 64
        secret_num %= modulo
        secret_num ^= math.floor(secret_num / 32)
        secret_num %= modulo
        secret_num ^= 2048 * secret_num
        secret_num %= modulo
        return secret_num

    seq = []
    for line in lines:
        a = int(line)
        r = []
        prev = a % 10
        for j in range(2000):
            n = gen_secret(a)
            r.append((n % 10 - prev % 10, n % 10))
            a = n
            prev = a
        ans += a
        seq.append(r)

    print("Part 1: ", ans)
    ans = 0

    dp = defaultdict(int)
    for _, s in enumerate(seq):
        seen = set()
        for j in range(len(s) - 4):
            key = tuple(x[0] for x in s[j : j + 4])
            val = s[j + 3][1]
            if (key) in seen:
                continue
            seen.add((key))
            dp[key] += val
    ans = max(dp.values())
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
