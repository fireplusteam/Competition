__YEAR__ = 2024
__DAY__ = 17
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

    def parseReg(line):
        line = utils.split_by_strings(r"Register |: ", line)
        return line[0], int(line[1])
    reg = {}
    for i in range(0, 3):
        reg_name, reg_val = parseReg(lines[i])
        reg[reg_name] = reg_val
    prog = [int(x) for x in utils.split_by_strings("Program: |,", lines[4])]
    print(reg)

    operand = {
        0: lambda: 0, 1: lambda: 1, 2: lambda: 2, 3: lambda: 3, 4: lambda: reg["A"], 5: lambda: reg["B"], 6: lambda: reg["C"]
    }

    res = []
    i = 0
    while i < len(prog):
        combo = operand[prog[i + 1]]()
        out = None
        print(prog[i], combo)
        match prog[i]:
            case 0:  # div
                r = reg["A"] // (2 ** combo)
                reg["A"] = r
                i += 2
            case 1:
                r = reg["B"] ^ prog[i + 1]
                reg["B"] = r
                i += 2
            case 2:
                r = combo % 8
                reg["B"] = r
                i += 2
            case 3:
                if reg["A"] != 0:
                    i = combo
                else:
                    r = None
                    i += 2
            case 4:
                r = reg["B"] ^ reg["C"]
                reg["B"] = r
                i += 2
            case 5:
                print("OUT", reg)
                r = combo % 8
                out = r
                i += 2
            case 6:
                r = reg["A"] // (2 ** combo)
                reg["B"] = r
                i += 2
            case 7:
                r = reg["A"] // (2 ** combo)
                reg["C"] = r
                i += 2

        print(reg)

        if out is not None:
            res.append(out)

    print(reg)
    print(prog)
    res = [str(x) for x in res]
    ans = ",".join(res)
    # Solution is here

    return ans


#  Test Cases -----------------------------------------------------------------------

def testCase(i, expected=None):
    utils.testCase(i, expected, lambda i, input: aoc_solver(i, input))


with open("src/output/output.txt", "w+") as file:
    sys.stdout = utils.writer(sys.stdout, file)

    testCase(1, "4,6,3,5,6,3,5,2,1,0")
    testCase(2, "4,2,5,6,7,7,7,7,3,1,0")
    # testCase(3)
    # testCase(4)
    # testCase(5)

    utils.download_content(__YEAR__, __DAY__)
    testCase("puzzle")
