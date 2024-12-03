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
import re

# Solution is here 




class Solver:

    def __init__(self):
        pass
    
    def solve(self, testCase):
        lines  = sys.stdin.read()
        res = 0 # here is method
        print(res)


if DEBUG:
    def redirect(i):
        file_path = f"src/input/input_{i}.txt"
        sys.stdin = open(file_path, 'r')
    
    def testCase(i):
        print("----------------------------------------------")
        print(f"Test Case #{i}:")
        redirect(i)
        solver = Solver()
        solver.solve(i)

    
#  Test Cases
testCase(1)
# testCase(2)

testCase("puzzle")