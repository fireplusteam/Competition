__YEAR__ = 2021
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
from functools import cmp_to_key

import sys
import fileinput
import re

import z3

import utils

# to run in Terminal: python3 src/python/main_py.py
# if output is to large: python3 src/python/main_py.py | less -R


def aoc_solver(testCase: int, input: str):
    scanners = input.strip().split("\n\n")

    scan_beacons = defaultdict(list)

    becons_points = set()
    for id, scanner in enumerate(scanners):
        scanner = scanner.strip().split("\n")
        for beacon in scanner[1:]:
            x, y, z = map(int, beacon.split(","))
            scan_beacons[id].append((x, y, z))
            becons_points.add((x, y, z))
    ans = len(becons_points)

    perm = None

    def get_permutaions():
        nonlocal perm
        if perm is not None:
            return perm
        p = set()

        def rotate(_x, _y, _z):
            p.add((_x, _y, _z))

        for _x, _y, _z in itertools.permutations([1, 2, 3]):
            for i in range(-1, 2, 2):
                for j in range(-1, 2, 2):
                    for k in range(-1, 2, 2):
                        rotate(_x * i, _y * j, _z * k)

        perm = list(p)
        return perm

    def transform(points):
        for a, b, c in get_permutaions():
            a_i = abs(a) - 1
            b_i = abs(b) - 1
            c_i = abs(c) - 1
            a_s = a // abs(a)
            b_s = b // abs(b)
            c_s = c // abs(c)
            r = []
            for point in points:
                x, y, z = point[a_i] * a_s, point[b_i] * b_s, point[c_i] * c_s
                r.append((x, y, z))
            # print(points)
            # print(r)
            yield r

    res_point = set()

    vis = set()
    scanners = set()

    def rec(id, points, x, y, z):
        nonlocal ans
        vis.add(id)
        for x1, y1, z1 in points:
            res_point.add((x + x1, y + y1, z + z1))
        scanners.add((x, y, z))

        # for id in range(len(scan_beacons)):
        for j in range(len(scan_beacons)):
            if j in vis:
                continue
            next_point = scan_beacons[j]
            for rotated in transform(next_point):
                dp = defaultdict(set)
                for x1, y1, z1 in points:
                    for x_1, y_1, z_1 in rotated:
                        n_x, n_y, n_z = x1 - x_1 + x, y1 - y_1 + y, z1 - z_1 + z
                        dp[(n_x, n_y, n_z)].add((x_1 + n_x, y_1 + n_y, z_1 + n_z))

                for k in dp.keys():
                    if len(dp[k]) >= 12:
                        ans -= len(dp[k])

                        # print("Match", id, len(dp[k]), (x, y, z), j, k)
                        rec(j, rotated, k[0], k[1], k[2])

    rec(0, scan_beacons[0], 0, 0, 0)
    print("Part 1: ", ans)

    ans = 0
    for x1, y1, z1 in scanners:
        for x2, y2, z2 in scanners:
            ans = max(ans, abs(x1 - x2) + abs(y1 - y2) + abs(z1 - z2))

    # Solution is here

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
