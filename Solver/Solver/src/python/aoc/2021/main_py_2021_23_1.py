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

        target = """...........
##A#B#C#D
 #A#B#C#D"""
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
                        to = chr(to + 2)
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
            "2": 1,
            "4": 10,
            "6": 100,
            "8": 1000
        }
        target_hash = utils.to_deep_hash(target)
        best_ans = 1e100

        seen = set()

        def rec(field, half, cost, deep=0):
            nonlocal best_ans
            moves = []
            should_continue = True
            while should_continue:
                should_continue = False
                for i in range(n):
                    m = len(field[i])
                    for j in range(m):
                        if field[i][j].isdigit() and half[i][j] == True:
                            ni, nj = i, j
                            delta_j = j_ind(field[i][j]) - j
                            while delta_j != 0:
                                nj += 1 if delta_j > 0 else -1
                                if not nj in range(len(field[ni])) or field[ni][nj] != '.':
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
                                if ni >= len(field) or field[ni][nj] != '.':
                                    break
                            ni -= 1
                            if (ni == 1 and field[ni + 1][nj] == field[i][j]) or (ni == 2):
                                should_continue = True
                                move_cost = cost_map[field[i][j]]
                                field[i][j], field[ni][nj] = field[ni][nj], field[i][j]
                                half[i][j] = False
                                cost += abs(i - ni) * \
                                    move_cost + abs(j - nj) * move_cost
                                moves.append((i, j, ni, nj))
                            field_hash = utils.to_deep_hash(field)
            # utils.debugPrint(field)
            # print(deep, "------------------")

            def restore():
                for i, j, ni, nj in moves:
                    field[i][j], field[ni][nj] = field[ni][nj], field[i][j]
                    assert (half[ni][nj] == False)
                    half[i][j] = True

            field_hash = utils.to_deep_hash(field)
            if field_hash == target_hash:
                if best_ans > cost:
                    best_ans = cost
                    print("Found", best_ans)
                restore()
                return
            if field_hash in seen:
                restore()
                return
            if best_ans <= cost:
                restore()
                return
            seen.add(field_hash)

            for i in range(n):
                m = len(field[i])
                for j in range(m):
                    if field[i][j].isdigit() and half[i][j] == False:
                        if i == 1 and j_ind(field[i][j]) == j and field[i + 1][j] == field[i][j]:
                            continue
                        if i == 2 and j_ind(field[i][j]) == j:
                            continue
                        ni, nj = i, j
                        while True:
                            ni -= 1
                            if ni < 0 or field[ni][nj] != '.':
                                break
                        ni += 1
                        if ni == i:
                            continue
                        for dj in (-1, 1):
                            nj = j
                            while True:
                                nj += dj
                                if not nj in range(0, len(field[ni])) or field[ni][nj] != '.':
                                    break
                                move_cost = cost_map[field[i][j]]
                                field[i][j], field[ni][nj] = field[ni][nj], field[i][j]
                                half[ni][nj] = True
                                rec(field, half, cost + abs(i - ni) *
                                    move_cost + abs(j - nj) * move_cost, deep + 1)
                                field[i][j], field[ni][nj] = field[ni][nj], field[i][j]
                                assert (half[ni][nj])
                                half[ni][nj] = False
                        continue

            restore()

            seen.remove(field_hash)
        half = utils.TwoD(n, len(target[0]), False)
        rec(field, half, 0)

        ans = best_ans

        return ans


#  Test Cases -----------------------------------------------------------------------

def testCase(i):
    solver = Solver()
    utils.testCase(i, lambda i, input: solver.solve(i, input))


# testCase(1)
# testCase(2)
# testCase(3)
# testCase(4)
# testCase(5)


utils.download_content(__YEAR__, __DAY__)
testCase("puzzle")
