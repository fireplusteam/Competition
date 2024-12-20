__YEAR__ = 2021
__DAY__ = 24
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
    instructions = input.strip().split("\n")
    instructions = [x.split(" ") for x in instructions]
    ans = 0
    # Solution is here
    input = []
    i = 0
    while i < len(instructions):
        if instructions[i][0] == "inp":
            r = []
            i += 1
            while i < len(instructions):
                if instructions[i][0] == "inp":
                    break
                r.append(instructions[i])
                i += 1
            input.append(r)
    instructions = input

    def simulate(w, z, depth):
        reg = {"x": 0, "y": 0, "z": z, "w": w}

        def num(b):
            if b in reg:
                return reg[b]
            return int(b)

        for i in instructions[depth]:
            instruct, a, b = i
            b = num(b)
            match instruct:
                case "add":
                    reg[a] += b
                case "mul":
                    reg[a] *= b
                case "div":
                    reg[a] //= b
                case "mod":
                    reg[a] %= b
                case "eql":
                    reg[a] = 1 if num(a) == b else 0
                case _:
                    assert False
        return reg["z"]

    @cache
    def rec(z, depth, part1):
        nonlocal number
        nonlocal res
        if depth == 14:
            if z < res:
                res = z
                print(res)
            return z == 0
        if z > 26 ** (14 - depth):
            return False

        list = range(9, 0, -1) if part1 else range(1, 10)

        for dig in list:
            next_z = simulate(dig, z, depth)

            if rec(next_z, depth + 1, part1):
                number = str(dig) + number
                return True
        return False

    number = ""
    res = 1e100
    rec(0, 0, True)
    print("Part 1:", number)

    number = ""
    res = 1e100
    rec(0, 0, False)
    ans = number

    return ans


#  Test Cases -----------------------------------------------------------------------


def testCase(i, expected=None):
    utils.testCase(i, expected, lambda i, input: aoc_solver(i, input))


with open("src/output/output.txt", "w+") as file:
    sys.stdout = utils.writer(sys.stdout, file)

    # testCase(1)
    # testCase(2)
    # testCase(3)
    # testCase(4)
    # testCase(5)

    utils.download_content(__YEAR__, __DAY__)
    testCase("puzzle")
