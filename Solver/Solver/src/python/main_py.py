DEBUG = True
# DEBUG = False 
#-----------------------------------------------------
from cmath import sqrt
import collections
import pprint
from queue import Queue
from collections import deque
from collections import OrderedDict
import sys
import fileinput, re

# Solution is here 

class Solver:
    
    def solve(self, testCase):
        T = int( input())
        print(T)



if DEBUG:
    def redirect(i):
        file_path = f"input_{i}.txt"
        sys.stdin = open(file_path, 'r')
    
    def testCase(i):
        print("----------------------------------------------")
        print(f"Test Case #{i}:")
        redirect(i)
        solver = Solver()
        solver.solve(i)

    
#  Test Cases
testCase(1)
testCase(2)

testCase("puzzle")