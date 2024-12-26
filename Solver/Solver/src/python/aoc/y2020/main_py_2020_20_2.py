__YEAR__ = 2020
__DAY__ = 20
#-----------------------------------------------------
import math
import os

import copy
import queue
import collections

from pprint import pprint
from queue import Queue
from queue import PriorityQueue

from collections import deque
from collections import OrderedDict
from collections import Counter
from collections import defaultdict

from sortedcontainers import SortedDict
from sortedcontainers import SortedSet
from sortedcontainers import SortedList

import sys
import fileinput, re

import utils

# to run in Terminal: python3 src/python/main_py.py
# if output is to large: python3 src/python/main_py.py | less -R
class Solver:
    def __init__(self):
        pass
    
    def solve(self, testCase: int, input: str):
        lines  = input.strip().split("\n\n")
        gr = defaultdict(set)
        render = {}
        def flip(projection, field2):
            n = len(field2)
            res = utils.TwoD(n, n, '.')
            for i in range(n):
                for j in range(n):
                    ni, nj = projection(i, j)
                    res[ni][nj] = field2[i][j]
            return res
        def calcHashes(field2):
            a = tuple(field2[0])
            c = tuple(field2[n - 1])
            d = tuple([field2[i][0] for i in range(n)])
            b = tuple([field2[i][n - 1] for i in range(n)])
            return (a, b, c, d)
        def getAll(field2): 
            n = len(field2)
            return [
                flip(lambda i, j: (i, j), field2),
                flip(lambda i, j: (j, i), field2),
                flip(lambda i, j: (j, n - i - 1), field2),
                flip(lambda i, j: (n - i - 1, j), field2),
                flip(lambda i, j: (i, n - j - 1), field2),
                flip(lambda i, j: (n - i - 1, n - j - 1), field2),
                flip(lambda i, j: (n - j - 1, n - i - 1), field2)
            ] 
        for field_case in lines:
            if len(field_case) == 0:
                break
            field_case = field_case.split("\n")
            n = 10
            pile_id = int(field_case[0].split(" ")[1].strip(":"))
            field = field_case[1:]

            for i in getAll(field):
                h = calcHashes(i)
                gr[pile_id].add(h) 
                if (pile_id, h) in render:
                    assert(False)
                render[(pile_id, h)] = i
        
        size = len(gr)
        size = int(math.sqrt(size))
        print(size)
        
        v_in = defaultdict(set)
        h_in = defaultdict(set)
        source = set()
        
        for id, i in gr.items():
            for j in i:
                a, b, c, d = j
                v_in[a].add(id)
                h_in[d].add(id)
                source.add((a, b, c, d, id))
        
        vis_id = set()
        vis_b = utils.TwoD(size, size, 0)
        vis_c = utils.TwoD(size, size, 0)
        vis_id_ind = utils.TwoD(size, size, 0)
        vis_a = utils.TwoD(size, size, 0)
        vis_d = utils.TwoD(size, size, 0)

        def add(id, i, j, a, b, c, d):
            if id in vis_id:
                assert(False)
            vis_id.add(id)
            vis_id_ind[i][j] = id 
            vis_a[i][j] = a
            vis_b[i][j] = b
            vis_c[i][j] = c 
            vis_d[i][j] = d
            
        def clear(id, i, j):
            vis_id.remove(id)
            vis_id_ind[i][j] = 0
            vis_a[i][j] = 0
            vis_b[i][j] = 0
            vis_c[i][j] = 0
            vis_d[i][j] = 0
        
        def getIJ():
            for i in range(size):
                for j in range(size):
                    if vis_b[i][j] == 0:
                        return (i, j)
            return None
        
        def draw():
            if (ij := getIJ()):
                i, j = ij
            else:
                return True
            if j > 0:
                # print(vis_id)
                b = vis_b[i][j - 1]
            else:
                b = None
            if j == 0:
                c = vis_c[i - 1][j]
            else:
                c = None

            # utils.debugPrint(b)
            if not b is None:
                horizontal = list(filter(lambda x: not x in vis_id, h_in[b]))
                if len(horizontal) == 0:
                    return False
            if not c is None:
                vertical = list(filter(lambda x: not x in vis_id, v_in[c]))
                if len(vertical) == 0:
                    return False
            if not b is None:
                for next_h_id in horizontal:
                    for _a, _b, _c, _d in gr[next_h_id]:
                        if b == _d and (c is None or c == _a):
                            add(next_h_id, i, j, _a, _b, _c, _d)
                            if draw():
                                return True
                            clear(next_h_id, i, j)
            elif not c is None:
                for next_v_id in vertical:
                    for _a, _b, _c, _d in gr[next_v_id]:
                        if c == _a and (b is None or b == _d):
                            add(next_v_id, i, j, _a, _b, _c, _d)
                            if draw():
                                return True
                            clear(next_v_id, i, j)
                            
            return False
                
        ans = 0
        for a, b, c, d, id in source:
            add(id, 0, 0, a, b, c, d)
            if draw():
                print("Found")
                ans = vis_id_ind[0][0] * vis_id_ind[0][-1] * vis_id_ind[-1][0] * vis_id_ind[-1][-1]
                break
            clear(id, 0, 0)
        
        mega_field = utils.TwoD(size * 8, size * 8, ".")
        for i in range(size):
            for j in range(size):
                # utils.debugPrint(vis_id_ind[i][j], vis_a[i][j], vis_b[i][j], vis_c[i][j], vis_d[i][j])
                f = render[(vis_id_ind[i][j], (vis_a[i][j], vis_b[i][j], vis_c[i][j], vis_d[i][j]))]
                assert(len(f) == 10)
                for _i in range(i * 8, (i + 1) * 8 ):
                    for _j in range(j * 8, (j + 1) * 8):
                        mega_field[_i][_j] = f[_i - i * 8 + 1][_j - j * 8 + 1]
                
        pattern = [
            "                  # ",
            "#    ##    ##    ###",
            " #  #  #  #  #  #   "
        ]
        
        for field_i in getAll(mega_field):
            ans = 0
            should_continue = True
            for i in range(len(field_i)):
                for j in range(len(field_i[0])):
                    if field_i[i][j] == '#':
                        ans += 1
                    is_valid = True
                    if i + 3 < len(field_i) and j + len(pattern[0]) < len(field_i[0]):
                        for k in range(0, len(pattern)):
                            for si, s in enumerate(pattern[k]):
                                if s == "#" and field_i[i + k][j + si] != '#':
                                    is_valid = False
                                    break
                            if not is_valid:
                                break
                    else:
                        is_valid = False
                    if is_valid:
                       ans -= 15 
                       should_continue = False
            if not should_continue:
                break
                
        # Solution is here
        
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