__YEAR__ = 2025
__DAY__ = 10
__TASK_ID__ = ""  # used for tests input prefix like __TASK_ID__ = "A"
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

from sympy import isprime

import sys
import fileinput
import re

# third parties
from z3 import z3

# import networkx

import utils
from utils import debugPrint
from utils import trace_recursive_calls

print = utils.printRec  # make recursive output with @trace_recursive_calls

# to run in Terminal: python3 src/python/solution.py < in.txt
# if output is to large: python3 src/python/solution.py < in.txt | less -R


def aoc_solver(testCase: int):
    input = sys.stdin.read().strip()
    # Input parser is here
    lines = input.split("\n")
    # print(lines)
    ans = 0
    n = len(lines)
    m = len(lines[0])
    print(n, m)

    def find(state, g):
        edgs = []
        for edg in g:
            r = [int(x.strip()) for x in edg.split(",") if len(x.strip()) > 0]
            if len(r) > 0:
                edgs.append(r)
        g = edgs
        # print(state, g)

        ret = 0
        x = []
        solve = z3.Optimize()

        for i in range(len(g)):
            _x = z3.Int("x" + str(i))
            x.append(_x)
            solve.add(_x >= 0)

        for i in range(len(state)):
            exp = []
            for j in range(len(g)):
                for _, k in enumerate(g[j]):
                    if i == k:
                        exp.append("x[" + str(j) + "]")
            exp = "+".join(exp)
            exp += "==" + str(state[i])
            # print(i, exp)
            z3_exp = eval(exp, globals(), locals())
            solve.add(z3_exp)

        exp = []
        for i in range(len(g)):
            exp.append("x[" + str(i) + "]")
        exp = "+".join(exp)
        exp = eval(exp, globals(), locals())

        result = solve.minimize(exp)

        if solve.check() == z3.sat:
            model = solve.model()
            for i in range(len(g)):
                _x = "x[" + str(i) + "]"
                _x = eval(_x, globals(), locals())
                ret += model[_x]
            print(state, ret)
            val = solve.lower(result)
            return val.as_long()
        else:
            assert False

    for line in lines:
        state, line = utils.split_by_strings(["\[|\]"], line)
        edgs = utils.split_by_strings("\(|\)", line)
        line = edgs[-1]
        state = line.replace("{", "").replace("}", "").strip().split(",")
        state = [int(x) for x in state]
        ans += find(state, edgs[:-1])

        # print(line)
    # Solution is here

    return ans


# run via terminal
if __name__ == "__main__":
    import time

    st = time.time()
    ans = aoc_solver(-1, input)
    print(f">  #Time = {time.time() - st: .5f}s")
    print(f">  {utils.Colors.WARNING}#Answer = {ans} {utils.Colors.ENDC}")
