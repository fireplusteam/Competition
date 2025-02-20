DEBUG = True
# DEBUG = False
# -----------------------------------------------------
from cmath import sqrt
import collections
from queue import Queue
from collections import deque
from collections import OrderedDict
import sys
import fileinput, re
import io, os

if DEBUG:
    file_path = "src/input/input_1.txt"
    sys.stdin = open(file_path, "r")

T = int(input())

for t in range(T):
    st = input().split()
    n, m = int(st[0]), int(st[1])
    a = [0] * n

    for i in range(n):
        a[i] = [int(x) for x in input().split()]

    def check(i, j, val):
        for di, dj in ((0, 1), (-1, 0), (0, -1), (1, 0)):
            ni, nj = i + di, j + dj
            if 0 <= ni < n and 0 <= nj < m and val == a[ni][nj]:
                return 2
        return 1

    def counter_from(counter):
        return 2 if counter >= 2 else counter

    dp = [0 for _ in range(n * m)]
    for i in range(n):
        for j in range(m):
            counter = check(i, j, a[i][j])
            dp[a[i][j] - 1] = max(dp[a[i][j] - 1], counter_from(counter))
    ans = sum(dp) - max(dp)
    print(ans)
