__YEAR__ = 2020
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

import utils

# to run in Terminal: python3 src/python/main_py.py
# if output is to large: python3 src/python/main_py.py | less -R


class Solver:
    def __init__(self):
        pass

    def solve(self, testCase: int, input: str):
        class LinkedList:
            def __init__(self, val):
                self.next = self
                self.prev = self
                self.val = val

            def delete(self):
                if self.prev != None:
                    self.prev.next = self.next
                    self.next.prev = self.prev
                    n = self.next
                    self.next = self.prev = None
                    return n
                else:
                    assert (False)

            def append(self, val):
                if self.next == None:
                    assert (False)
                else:
                    first = self.next
                    self.next = LinkedList(val)
                    self.next.next = first
                    self.next.prev = self
                    first.prev = self.next

                return self.next

            def to_list(self):
                first = self.next
                l = [[self.prev.val, self.val, self.next.val]]

                while first != self:
                    l.append([first.prev.val, first.val, first.next.val])
                    # l.append(first.val)
                    first = first.next
                return l

        line = [int(x) for x in input.strip()]
        ans = 0
        # Solution is here
        n = len(line)
        # for i in range(10, 1000000 + 1):
        #     line.append(i)
        max_val = max(line)

        d_line = LinkedList(line[0])
        inverse_line = {line[0]: d_line}
        for i, val in enumerate(line):
            if i > 0:
                d_line = d_line.append(val)
                inverse_line[val] = d_line

        line = d_line.next
        # print(line.to_list())

        def getInd(val):
            return inverse_line[val]

        def move(current_ind: LinkedList):
            current_label = current_ind.val
            # print("current_label", current_label)

            def cut(ind: LinkedList):
                inside = []
                ind = ind.next
                for i in range(3):
                    val = ind.val
                    inside.append(val)
                    ind = ind.delete()
                    del inverse_line[val]
                return inside, ind

            inside, outer = cut(current_ind)
            inside_set = set(inside)
            destination_label = current_label - 1

            # print("current_label", current_ind.to_list())
            # print(inside, outer.to_list())

            while True:
                if destination_label < 1:
                    destination_label = max_val
                if not destination_label in inside_set:
                    break
                destination_label -= 1

            # print("dest_label", destination_label)

            destination_index = getInd(destination_label)

            for i in range(3):
                val = inside[i]
                destination_index = destination_index.append(val)
                inverse_line[val] = destination_index

            current_ind = getInd(current_label).next
            # print(current_ind.to_list())

            return current_ind

        ind = line
        for step in range(100):
            ind = move(ind)
            # print(ind.to_list())

        ind = getInd(1).next
        res = ""
        for i in range(n - 1):
            res += str(ind.val)
            ind = ind.next

        print(line)
        ans = res

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
