__YEAR__ = 2021
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

# to run in Terminal: python3 src/python/main_py.py
# if output is to large: python3 src/python/main_py.py | less -R


def aoc_solver(testCase: int, input: str):
    lines = input.strip().split("\n")
    on_dp = set()
    for t, line in enumerate(lines):
        line = utils.split_by_strings(r" |x=|y=|z=|,|\.\.", line)
        print(line)
        operation = line[0]
        line = [int(line[i]) for i in range(1, len(line))]

        print(line)
        x1, y1, z1 = [x for i, x in enumerate(line) if i % 2 == 0]
        x2, y2, z2 = [x for i, x in enumerate(line) if i % 2 == 1]
        if x1 > x2:
            x1, x2 = x2, x1
        if y1 > y2:
            y1, y2 = y2, y1
        if z1 > z2:
            z1, z2 = z2, z1

        def cut(cub1, cub2):  # cub1 - cub2 as union
            x1, y1, z1, x2, y2, z2 = cub1
            _x1, _y1, _z1, _x2, _y2, _z2 = cub2

            com_x1 = max(_x1, x1)
            com_x2 = min(_x2, x2)
            com_y1 = max(_y1, y1)
            com_y2 = min(_y2, y2)
            com_z1 = max(_z1, z1)
            com_z2 = min(_z2, z2)
            if com_x2 - com_x1 < 0 or com_y2 - com_y1 < 0 or com_z2 - com_z1 < 0:
                return None

            def is_valid_cub(cube):
                assert len(cube) // 2 == 3
                for i in range(0, len(cube) // 2):
                    if cube[i] > cube[i + 3]:
                        return False
                return True

            res = []

            up_x = [x1, y1, z1, com_x1 - 1, y2, z2]
            down_x = [com_x2 + 1, y1, z1, x2, y2, z2]

            up_y = [x1, y1, z1, x2, com_y1 - 1, z2]
            down_y = [x1, com_y2 + 1, z1, x2, y2, z2]

            up_z = [x1, y1, z1, x2, y2, com_z1 - 1]
            if is_valid_cub(up_z):
                res.append(up_z)
                for i in [up_x, down_x, up_y, down_y]:
                    i[2] = com_z1  # update z

            down_z = (x1, y1, com_z2 + 1, x2, y2, z2)
            if is_valid_cub(down_z):
                res.append(down_z)
                for i in [up_x, down_x, up_y, down_y]:
                    i[5] = com_z2  # update z
            if is_valid_cub(up_x):
                res.append(up_x)
                for i in [up_y, down_y]:
                    i[0] = com_x1  # update x
            if is_valid_cub(down_x):
                res.append(down_x)
                for i in [up_y, down_y]:
                    i[3] = com_x2  # update x
            if is_valid_cub(up_y):
                res.append(up_y)
            if is_valid_cub(down_y):
                res.append(down_y)
            return [tuple(x) for x in res]

        new_cube = (x1, y1, z1, x2, y2, z2)
        if operation == "on":
            left = {new_cube}
            for on_cube in on_dp:
                next_left = set()
                for left_cube in left:
                    r = cut(left_cube, on_cube)
                    if r is None:
                        next_left.add(left_cube)
                    else:
                        next_left |= set(r)

                left = next_left
            on_dp |= left
        else:
            next_dp = set()
            for on_cube in on_dp:
                r = cut(on_cube, new_cube)
                if r is None:
                    next_dp.add(on_cube)
                else:
                    next_dp |= set(r)
            on_dp = next_dp

    ans = 0
    for x1, y1, z1, x2, y2, z2 in on_dp:
        assert x1 <= x2
        assert y1 <= y2
        assert z1 <= z2
        ans += (x2 - x1 + 1) * (y2 - y1 + 1) * (z2 - z1 + 1)

    return ans


#  Test Cases -----------------------------------------------------------------------


def testCase(i, expected=None):
    utils.testCase(i, expected, lambda i, input: aoc_solver(i, input))


with open("src/output/output.txt", "w+") as file:
    sys.stdout = utils.writer(sys.stdout, file)

    testCase(1, 2758514936282235)
    # testCase(2)
    # testCase(3)
    # testCase(4)
    # testCase(5)

    utils.download_content(__YEAR__, __DAY__)
    testCase("puzzle")
