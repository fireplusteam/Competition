__YEAR__ = 2024
__DAY__ = 4

DEBUG = True
# DEBUG = False 
#-----------------------------------------------------
import cmath

import copy
import queue
import collections

from pprint import pprint
from queue import Queue
from queue import PriorityQueue

from collections import deque
from collections import OrderedDict
from collections import Counter

from sortedcontainers import SortedDict
from sortedcontainers import SortedSet
from sortedcontainers import SortedList

import sys
import fileinput, re


class Solver:
    def __init__(self):
        pass
    
    def solve(self, testCase):
        lines  = sys.stdin.read().strip()
        ans = 0
        # Solution is here
        
        return ans


if DEBUG:
    def redirect(i):
        file_path = f"src/input/input_{i}.txt"
        sys.stdin = open(file_path, 'r')
    
    def testCase(i):
        print("----------------------------------------------")
        print(f"Test Case #{i}:")
        redirect(i)
        solver = Solver()
        ans = solver.solve(i)
        print(f"  #{i} Answer = {ans}")

    
#  Test Cases
testCase(1)
# testCase(2)

# ------------------------------------ download input script
# python3 src/python/helper/get_input.py --year=2024 --day=3 > src/input/input_puzzle.txt
import subprocess
import os
def download_content():
    cache_path = "src/python/helper/cache.txt"
    mode = "w+" if not os.path.exists(cache_path) else "r"
    with open(cache_path, mode) as file:
        is_downloaded = file.read()
    with open(cache_path, "w+") as file:
        identity = f"Year:{__YEAR__},Day:{__DAY__}"
        if is_downloaded != identity:
            process = subprocess.run(["python3", f"src/python/helper/get_input.py", f"--year={__YEAR__}", f"--day={__DAY__}"], stdout=subprocess.PIPE)
            with open("src/input/input_puzzle.txt", "wb+") as puzzle:
                if not b"Please don't repeatedly request this endpoint" in process.stdout:
                    puzzle.write(process.stdout)
                    file.write(identity)
                else:
                    file.write("")
                    puzzle.write(b"")
        else:
            file.write(identity)

download_content()
testCase("puzzle")