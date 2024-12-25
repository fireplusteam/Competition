__YEAR__ = 2022
__DAY__ = 19
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
# from z3 import z3
# import networkx

import utils
from utils import debugPrint
from utils import trace_recursive_calls

print = utils.printRec  # make recursive output with @trace_recursive_calls

# to run in Terminal: python3 src/python/main_py.py
# if output is to large: python3 src/python/main_py.py | less -R


def aoc_solver(testCase: int, input: str):
    lines = input.strip().split("\n")
    ans = 0
    # Solution is here

    for b_id, blueprint in enumerate(lines):
        print(blueprint)

        def parse(s):
            p = re.findall(r"\d+", s)
            return [int(x) for x in p]

        nums = parse(blueprint)

        costs = {}
        nums = nums[1:]
        costs[0] = [(0, nums[0])]
        costs[1] = [(0, nums[1])]
        costs[2] = [(0, nums[2]), (1, nums[3])]
        costs[3] = [(0, nums[4]), (2, nums[5])]

        q = utils.MaxHeap(None, key=lambda x: (x[2][3], x[1][3], x[1][2], x[1][1]))
        q.put((0, (1, 0, 0, 0), (0, 0, 0, 0)))  # day, rob, res
        seen = set()

        ind = 0
        best = 0
        time_end = 24
        while len(q) > 0:
            day, robots, resources = q.get()

            def harvest(robots, resources):
                r = resources.copy()
                for i, j in enumerate(robots):
                    r[i] += j
                return r

            def determine_max_buy(robot_index, resources):
                max_bought = 1e10
                for j, cost in costs[robot_index]:
                    max_bought = min(max_bought, resources[j] // cost)
                return max_bought

            def estimate():
                rob = list(robots)
                res = list(resources)
                for _ in range(day + 1, time_end + 1):
                    next_res = harvest(rob, res)
                    for i in range(len(rob)):
                        if determine_max_buy(i, res) > 0:
                            rob[i] += 1

                    res = next_res
                return res[3]

            if best < resources[3]:
                best = resources[3]
                print(b_id + 1, best)
                # print(day, robots, resources)
            if best >= estimate():
                continue
            ind += 1

            def adj(n_resources, robots: tuple):
                def adj(n_resources: list, robots: tuple, n_robots):
                    if n_robots[0] > 4 or n_robots[1] > 10 or n_robots[2] > 12:
                        return
                    buy = 0
                    for i in range(3, -1, -1):
                        can_be_bought = determine_max_buy(i, n_resources)
                        if can_be_bought > 0:
                            for j, cost in costs[i]:
                                n_resources[j] -= cost
                            n_robots[i] += 1
                            yield tuple(n_robots), tuple(harvest(robots, n_resources))
                            for j, cost in costs[i]:
                                n_resources[j] += cost
                            n_robots[i] -= 1
                            buy += 1
                            if buy >= 2:  # try to build only two last robots
                                return

                    yield tuple(n_robots), tuple(harvest(robots, n_resources))

                yield from adj(n_resources.copy(), robots, list(robots))

            n_resources = list(resources)
            for day_offset in range(day + 1, min(day + 3, time_end + 1)):
                for n_rob, n_res in adj(n_resources, list(robots)):
                    key = hash((day_offset, n_rob, n_res))
                    if key not in seen:
                        q.put((day_offset, n_rob, n_res))
                        seen.add(key)
                n_resources = harvest(robots, n_resources)
        ans += (b_id + 1) * best

    return ans


#  Test Cases -----------------------------------------------------------------------


def testCase(i, expected=None):
    utils.testCase(i, expected, lambda i, input: aoc_solver(i, input))


sys.setrecursionlimit(10**6)

with open("src/output/output.txt", "w+") as file:
    sys.stdout = utils.writer(sys.stdout, file)

    testCase(1)
    # testCase(2)
    # testCase(3)
    # testCase(4)
    # testCase(5)

    utils.download_content(__YEAR__, __DAY__)
    testCase("puzzle")
