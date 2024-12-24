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
# from graphviz import Digraph  # to visualize the graph

import utils
from utils import printRec
from utils import debugPrint
from utils import trace_recursive_calls

# to run in Terminal: python3 src/python/main_py.py
# if output is to large: python3 src/python/main_py.py | less -R


# class GraphVisualization:

#     def __init__(self):
#         self.visual = []

#     def addEdge(self, a, b, label):
#         temp = [a, b, label]
#         self.visual.append(temp)

#     def visualize(self):
#         dot = Digraph()
#         for a, b, label in self.visual:
#             dot.edge(a, b, label=label)
#         dot.render("output", view=True, format="png")


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
    undirected_g = defaultdict(set)

    for g in gates.split("\n"):
        command, out = g.split(" -> ")
        a, com, b = command.split(" ")
        gr_g[out] = (a, com, b)
        undirected_g[out].add(a)
        undirected_g[out].add(b)
        undirected_g[a].add(out)
        undirected_g[b].add(out)
        if out.startswith("z"):
            max_z = max(out, max_z)

    def swap(i, j):
        k1 = keys[i]
        k2 = keys[j]

        def remove(u):
            a, _, b = gr_g[u]
            undirected_g[u].discard(a)
            undirected_g[u].discard(b)
            undirected_g[a].discard(u)
            undirected_g[b].discard(u)

        def add(u):
            a, _, b = gr_g[u]
            undirected_g[a].add(u)
            undirected_g[b].add(u)
            undirected_g[u].add(a)
            undirected_g[u].add(b)

        remove(k1)
        remove(k2)

        gr_g[k1], gr_g[k2] = gr_g[k2], gr_g[k1]

        add(k1)
        add(k2)

    def get_closest(graph: defaultdict(set), i, max_dist=3):
        u = keys[i]

        q = Queue()
        q.put((u, 0))
        seen = set()
        r = set()
        while not q.empty():
            u, cost = q.get()
            if cost > max_dist:
                return r
            if u != keys[i]:
                if k := order_of_key(u):
                    r.add(k)

            for v in graph[u]:
                if v not in seen:
                    seen.add(v)
                    q.put((v, cost + 1))
        return r

    keys = sorted(list(gr_g.keys()))

    def order_of_key(key):
        i = bisect.bisect(keys, key)
        if i:
            return i - 1
        return None

    # vis_graph = GraphVisualization()
    # for out, (a, com, b) in gr_g.items():
    #     vis_graph.addEdge(out, a, com)
    #     vis_graph.addEdge(out, b, com)
    # vis_graph.visualize()

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

    dfs_dp = {}

    def dfs(v, root_z):
        nonlocal dfs_dp
        dfs_dp = {}
        return _dfs(v, root_z)

    def _dfs(v, root_z):
        if v in dfs_dp:
            if dfs_dp[v] == -1:
                raise "Error"
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
                raise f"Wrong swap {v} for z: {root_z}"
            r = gr_w[v]
            dfs_dp[v] = r
            return r
        assert False

    count_cache = {}

    def _check_configuration(z, carry):
        nonlocal count_cache
        if z == max_z + 1:
            return carry == 0
        if (z, carry) in count_cache:
            return count_cache[(z, carry)]
        if z > max_x:
            coor_z = to_coordinate("z", z)
            r = carry == dfs(coor_z, coor_z)
            count_cache[(z, carry)] = r
            return r

        for x in range(0, 2):
            for y in range(0, 2):
                gr_w[to_coordinate("x", z)] = x
                gr_w[to_coordinate("y", z)] = y
                addition = x + y + carry  # x & y  # & carry
                coor_z = to_coordinate("z", z)
                res = dfs(coor_z, coor_z)
                if res == addition % 2:
                    if _check_configuration(z + 1, addition // 2) == False:
                        count_cache[(z, carry)] = False
                        return False
                else:
                    count_cache[(z, carry)] = False
                    return False

        count_cache[(z, carry)] = True
        return True

    def check_configuration(z):
        nonlocal count_cache
        count_cache = {}
        return _check_configuration(z, 0)

    found_pairs = ()

    def find_swaps(not_valid_z: list, num_of_tries: int, pairs: set):
        nonlocal found_pairs
        if num_of_tries == 4:
            try:
                if check_configuration(0) == True:
                    found_pairs = pairs
                    return True
            except:
                pass
            return False

        if num_of_tries < len(not_valid_z):
            i_list = [order_of_key(not_valid_z[num_of_tries])]
        else:
            i_list = range(len(gr_g))

        for i in i_list:
            if i in pairs:
                continue
            all = get_closest(undirected_g, i)
            for j in all:
                if j in pairs:
                    continue
                if num_of_tries < len(not_valid_z) and gr_g[keys[j]][1] != "XOR":
                    continue

                swap(i, j)
                if find_swaps(not_valid_z, num_of_tries + 1, pairs | {i, j}):
                    return True
                swap(i, j)
        return False

    def find_all_not_valid_z():  # z which has NOT XOR operation
        res_list = []
        for k, (a, com, b) in gr_g.items():
            if k.startswith("z") and com != "XOR" and int(k[1:]) != max_z:
                res_list.append(k)
        return res_list

    find_swaps(find_all_not_valid_z(), 0, set())

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
