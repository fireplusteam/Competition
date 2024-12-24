__YEAR__ = 2024
__DAY__ = 24
# -----------------------------------------------------
import bisect
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


def aoc_solver(testCase: int, input: str):
    wire, gates = input.strip().split("\n\n")
    ans = 0
    # Solution is here

    gr_w = {}
    max_z = ""
    max_x = ""
    max_y = ""
    for w in wire.split("\n"):
        name, value = w.split(": ")
        gr_w[name] = int(value)
        if name.startswith("x"):
            max_x = max(max_x, name)
        if name.startswith("y"):
            max_y = max(max_y, name)

    gr_g = {}

    for g in gates.split("\n"):
        command, out = g.split(" -> ")
        a, com, b = command.split(" ")
        gr_g[out] = (a, com, b)
        if out.startswith("z"):
            max_z = max(out, max_z)

    def swap(i, j):
        k1 = keys[i]
        k2 = keys[j]
        gr_g[k1], gr_g[k2] = gr_g[k2], gr_g[k1]

    keys = sorted(list(gr_g.keys()))

    def order_of_key(key):
        i = bisect.bisect(keys, key)
        if i:
            return i - 1
        return None

    def num_name(a):
        return int(a[1:])

    def to_coordinate(prefix, a):
        return f"{prefix}{a:02d}"

    max_x = num_name(max_x)
    max_y = num_name(max_y)
    max_z = num_name(max_z)

    def com_res(a, com, b):
        match com:
            case "AND":
                return a & b
            case "OR":
                return a | b
            case "XOR":
                return a ^ b
        assert False

    def dfs(v, root_z):
        dfs_dp = {}

        def _dfs(v, root_z):
            if v in dfs_dp:
                if dfs_dp[v] == -1:
                    raise Exception("Error, there's a loop")
                return dfs_dp[v]
            dfs_dp[v] = -1
            if v in gr_g:
                a, com, b = gr_g[v]
                a = _dfs(a, root_z)
                b = _dfs(b, root_z)
                r = com_res(a, com, b)
                dfs_dp[v] = r
                return r
            if v in gr_w:
                if v[1:] > root_z[1:]:
                    raise Exception(f"Wrong swap {v} for z: {root_z}")
                r = gr_w[v]
                dfs_dp[v] = r
                return r
            assert False

        return _dfs(v, root_z)

    class Ex(BaseException):
        def __init__(self, val):
            self.z = val

    def check_configuration(z):
        count_cache = {}

        def _check_configuration(z, carry):
            nonlocal count_cache
            if z == max_z + 1:
                return carry == 0
            if (z, carry) in count_cache:
                return count_cache[(z, carry)]
            if z > max_x:
                coor_z = to_coordinate("z", z)
                valid_pairs = carry == dfs(coor_z, coor_z)
                count_cache[(z, carry)] = valid_pairs
                return valid_pairs

            valid_pairs = []
            for x in range(0, 2):
                for y in range(0, 2):
                    gr_w[to_coordinate("x", z)] = x
                    gr_w[to_coordinate("y", z)] = y
                    addition = x + y + carry  # x & y  # & carry
                    coor_z = to_coordinate("z", z)
                    res = dfs(coor_z, coor_z)
                    if res != addition % 2:
                        count_cache[(z, carry)] = False
                        raise Ex(z)
                    valid_pairs.append((x, y, res))

            for x, y, res in valid_pairs:
                if _check_configuration(z + 1, addition // 2) == False:
                    count_cache[(z, carry)] = z
                    return False

            count_cache[(z, carry)] = True
            return True

        return _check_configuration(0, 0)

    found_pairs = ()

    def find_swaps(num_of_tries: int, pairs: set):
        nonlocal found_pairs
        invalid_z = None
        list_of_pairs = []

        for i in range(len(gr_g)):
            if i in pairs:
                continue
            for j in range(i + 1, len(gr_g)):
                if j in pairs:
                    continue

                swap(i, j)
                try:
                    if check_configuration(0):
                        found_pairs = pairs | {i, j}
                        return True
                except Ex as e:
                    zz = f"z{e.z:2d}"
                    if invalid_z == None or invalid_z <= zz:
                        if invalid_z == None or invalid_z < zz:
                            list_of_pairs = []
                        list_of_pairs.append((i, j))
                        invalid_z = zz
                except:  # not valid circuit
                    pass
                swap(i, j)
        if invalid_z:
            for i, j in list_of_pairs:
                swap(i, j)
                if find_swaps(num_of_tries + 1, pairs | {i, j}):
                    return True
                swap(i, j)
        assert invalid_z == None
        return False

    find_swaps(0, set())

    ans = [keys[i] for i in found_pairs]
    return ",".join(sorted(ans))


#  Test Cases -----------------------------------------------------------------------


def testCase(i, expected=None):
    utils.testCase(i, expected, lambda i, input: aoc_solver(i, input))


sys.setrecursionlimit(10**6)

with open("src/output/output.txt", "w+") as file:
    sys.stdout = utils.writer(sys.stdout, file)

    # testCase(1, "z00,z01,z02,z05")
    # testCase(2, 2024)
    # testCase(3)
    # testCase(4)
    # testCase(5)

    utils.download_content(__YEAR__, __DAY__)
    testCase("puzzle")
