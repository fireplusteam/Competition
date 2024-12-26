__YEAR__ = 2024
__DAY__ = 15
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
        field, moves = input.strip().split("\n\n")

        moves = moves.replace("\n", "")
        field = [[x for x in y] for y in field.split("\n")]

        ans = 0
        # Solution is here
        dir = {
            ">": (0, 1),
            "<": (0, -1),
            "^": (-1, 0),
            "v": (1, 0)
        }
        n = len(field)
        m = len(field[0])

        def map_to_large():
            buff = []
            for i in range(n):
                b = []
                for j in range(m):
                    if field[i][j] == '@':
                        b.append("@")
                        b.append(".")
                    elif field[i][j] == 'O':
                        b.append("[")
                        b.append("]")
                    else:
                        b.append(field[i][j])
                        b.append(field[i][j])
                buff.append(b)
            return buff
        field = map_to_large()
        n = len(field)
        m = len(field[0])

        def simulate(ri, rj):
            for step in moves:
                di, dj = dir[step]
                # print("Step", step)

                def rec_move(ri, rj, modify):
                    def swap(i, j, ni, nj):
                        if modify:
                            field[i][j], field[ni][nj] = field[ni][nj], field[i][j]
                    ni, nj = ri + di, rj + dj
                    if field[ni][nj] == '#':
                        return False
                    elif field[ni][nj] == ']' or field[ni][nj] == '[':
                        if abs(dj) == 1:
                            if rec_move(ni, nj + dj, modify):
                                swap(ni, nj, ni, nj + dj)
                                swap(ri, rj, ni, nj)
                                return True
                        else:
                            if field[ni][nj] == '[':
                                if rec_move(ni, nj, modify) and rec_move(ni, nj + 1, modify):
                                    swap(ri, rj, ni, nj)
                                    return True
                            elif field[ni][nj] == ']':
                                if rec_move(ni, nj, modify) and rec_move(ni, nj - 1, modify):
                                    swap(ri, rj, ni, nj)
                                    return True
                            return False
                    elif field[ni][nj] == '.':
                        swap(ri, rj, ni, nj)
                        return True
                    return False
                if rec_move(ri, rj, False):
                    rec_move(ri, rj, True)
                    ri, rj = ri + di, rj + dj
                    assert (field[ri][rj] == '@')

        for i in range(n):
            is_ = False
            for j in range(m):
                if field[i][j] == '@':
                    simulate(i, j)
                    is_ = True
                    break
            if is_:
                break
        for i in range(n):
            for j in range(m - 1):
                if field[i][j] == '[' and field[i][j + 1] == ']':
                    ans += 100 * i + j

        return ans


#  Test Cases -----------------------------------------------------------------------

def testCase(i):
    solver = Solver()
    utils.testCase(i, lambda i, input: solver.solve(i, input))


with open("output.txt", "w+") as file:
    sys.stdout = file

    testCase(1)
    # testCase(2)
    # testCase(3)
    # testCase(4)
    # testCase(5)

    utils.download_content(__YEAR__, __DAY__)
    testCase("puzzle")
