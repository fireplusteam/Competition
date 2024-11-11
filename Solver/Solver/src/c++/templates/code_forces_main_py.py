DEBUG = True
# DEBUG = False 
#-----------------------------------------------------
from cmath import sqrt
import collections
from queue import Queue
from collections import deque
from collections import OrderedDict
import sys
import fileinput, re

if DEBUG:
    file_path = "../input/input.txt"
    sys.stdin = open(file_path, 'r')

T = int(input())

for t in range(T):
    n = int(input())
    a = [int(x) for x in input().split()]
    a = [x if i % 2 == 0 else -x for i, x in enumerate(a)]
    sumer = OrderedDict()
    sumer[0] = 1
    sum = 0
    is_ok = False
    for x in a:
        sum += x
        if sum in sumer:
            is_ok = True
            break
        sumer[sum] = 1
    if is_ok:
        print("YES")
    else:
        print("NO")