__YEAR__ = 2021
__DAY__ = 23
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

import z3

import utils

# to run in Terminal: python3 src/python/main_py.py
# if output is to large: python3 src/python/main_py.py | less -R


class Solver:
    def __init__(self):
        pass

    def solve(self, testCase: int, input: str):
        field = input.strip().split("\n")
        field = [[x for x in y] for y in field]
        d = ((-1, 0), (1, 0), (0, -1), (0, 1))

        target = """#############
#...........#
###A#B#C#D###
  #A#B#C#D#
  #########"""
        target = [[x for x in y] for y in target.split("\n")]
        n = len(field)

        utils.debugPrint(field)

        def mapp(field: list[list[str]]):
            for i in range(n):
                m = len(field[i])
                for j in range(m):
                    if field[i][j].isalpha():
                        to = ord(field[i][j]) - ord("A")
                        to *= 2
                        to += ord("0")
                        to = chr(to + 3)
                        field[i][j] = to
            return field
        field = mapp(field)
        target = mapp(target)

        utils.debugPrint(field)
        utils.debugPrint(target)

        def j_ind(ch: str):
            if ch.isdigit():
                return ord(ch) - ord("0")
            return -1

        cost_map = {
            "3": 1,
            "5": 10,
            "7": 100,
            "9": 1000
        }

        def to_hash(field):
            r = ""
            for j in range(1, len(field[0]) - 1):
                r += field[1][j]
            for i in range(2, len(field) - 1):
                for j in range(3, 10, 2):
                    r += field[i][j]
            return r

        target_hash = to_hash(target)
        best_ans = 1e100

        seen = {}

        def rec(cost, deep=0):
            nonlocal best_ans
            moves = []
            should_continue = True
            pre_move_cost = 0
            while should_continue:
                should_continue = False
                i = 1
                m = len(field[i])
                for j in range(m):
                    if field[i][j].isdigit():
                        ni, nj = i, j
                        delta_j = j_ind(field[i][j]) - j
                        while delta_j != 0:
                            nj += 1 if delta_j > 0 else -1
                            if field[ni][nj] != '.':
                                break
                            if nj == j_ind(field[i][j]):
                                nj += 1 if delta_j > 0 else -1
                                break
                        if delta_j != 0:
                            nj -= 1 if delta_j > 0 else -1
                        if nj != j_ind(field[i][j]):
                            continue

                        while True:
                            ni += 1
                            if field[ni][nj] != '.':
                                break
                        ni -= 1
                        if (ni == 2 and field[ni + 1][nj] == field[i][j]) or (ni == 3):
                            should_continue = True
                            move_cost = cost_map[field[i][j]]
                            field[i][j], field[ni][nj] = field[ni][nj], field[i][j]
                            pre_move_cost += abs(i - ni) * \
                                move_cost + abs(j - nj) * move_cost
                            moves.append((i, j, ni, nj))
            # utils.debugPrint(field)
            # print(deep, "------------------")

            def restore():
                for i, j, ni, nj in moves:
                    field[i][j], field[ni][nj] = field[ni][nj], field[i][j]

            field_hash = to_hash(field)
            cost += pre_move_cost
            if field_hash == target_hash:
                if best_ans > cost:
                    best_ans = cost
                    print("Found", best_ans)
                restore()
                return pre_move_cost
            if field_hash in seen:
                if best_ans > cost + seen[field_hash]:
                    # utils.debugPrint(field)
                    best_ans = cost + seen[field_hash]
                    print("Found", best_ans)
                restore()
                return seen[field_hash] + pre_move_cost
            if best_ans <= cost:
                restore()
                return 1e100
            ret = 1e100
            seen[field_hash] = ret
            for i in range(2, n - 1):
                m = len(field[i])
                for j in range(3, m, 2):
                    if field[i][j].isdigit():
                        if i == 2 and j_ind(field[i][j]) == j and field[i + 1][j] == field[i][j]:
                            continue
                        if i == 3 and j_ind(field[i][j]) == j:
                            continue
                        ni, nj = i, j
                        while True:
                            ni -= 1
                            if field[ni][nj] != '.':
                                break
                        ni += 1
                        if ni != 1:
                            continue
                        for dj in (-1, 1):
                            nj = j
                            while True:
                                nj += dj
                                if field[ni][nj] != '.':
                                    break
                                if nj != j:
                                    move_cost = cost_map[field[i][j]]
                                    field[i][j], field[ni][nj] = field[ni][nj], field[i][j]
                                    cost_delta = abs(
                                        i - ni) * move_cost + abs(j - nj) * move_cost
                                    lr = rec(cost + cost_delta, deep + 1)
                                    ret = min(lr + cost_delta, ret)
                                    field[i][j], field[ni][nj] = field[ni][nj], field[i][j]
                        continue

            restore()
            seen[field_hash] = ret
            return ret + pre_move_cost

        rec(0)

        ans = best_ans

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
