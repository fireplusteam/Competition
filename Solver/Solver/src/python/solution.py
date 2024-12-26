__YEAR__ = 2024
__DAY__ = 10
__TASK_ID__ = ""  # used for tests input prefix like __TASK_ID__ = "A"
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

# to run in Terminal: python3 src/python/solution.py < in.txt
# if output is to large: python3 src/python/solution.py < in.txt | less -R


def aoc_solver(testCase: int, input: str):
    input = sys.stdin.read().strip()
    lines = input.split("\n")
    ans = 0
    # Solution is here
    print(input)

    return ans


# run via terminal
if __name__ == "__main__":
    import time

    st = time.time()
    ans = aoc_solver(-1, input)
    print(f">  #Time = {time.time() - st: .5f}s")
    print(f">  {utils.Colors.WARNING}#Answer = {ans} {utils.Colors.ENDC}")
