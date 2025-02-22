DEBUG = True
# -----------------------------------------------------
from cmath import sqrt
import collections
from queue import Queue
from collections import defaultdict, deque
from collections import OrderedDict
import sys
import re


def debugPrint(*values: object, sep=" ", end="\n", file=None, flush=False):
    print(*values, sep=sep, end=end, file=file, flush=flush)


def _debugPrint(*values: object, sep=" ", end="\n", file=None, flush=False):
    pass


if "DEBUG" in globals() and DEBUG:
    sys.stdin = open("src/input/input_1.txt", "r")
else:
    debugPrint = _debugPrint


# ------------ Test Case Solver, solution is here ----------------
def case_solver():
    s = input()
    a, b, ab, ba = [int(x) for x in input().split()]
    debugPrint(s, a, b, ab, ba)

    i = 0
    common_collections = []
    ab_collections = []
    ba_collections = []

    def calculate_score(i, j):
        n = j - i
        score = n >> 1
        if n % 2 == 1:
            return (score, 0, s[i] == "A", s[i] == "B")
        else:
            return (score if s[i] == "A" else 0, score if s[i] == "B" else 0, 0, 0)

    while i < len(s):
        j = i + 1
        while j < len(s) and s[j - 1] != s[j]:
            j += 1

        n = j - i
        if n == 1:
            if s[i] == "A":
                a -= 1
            else:
                b -= 1
        elif n % 2 == 1:
            common_collections.append(calculate_score(i, j))
        else:
            score = calculate_score(i, j)
            if score[0] != 0:
                ab_collections.append(score)
            else:
                ba_collections.append(score)

        i = j
    ab_collections.sort()
    ba_collections.sort()
    # print("AB_collections", ab_collections)
    # print("BA_collections", ba_collections)
    # print("Common_collections", common_collections)
    for ab_score, _, _, _ in ab_collections:
        if ab - ab_score >= 0:
            ab -= ab_score
            ab_score = 0
        elif ab > 0:
            ab_score -= ab
            ab = 0
        if ab_score > 1:
            if ba - ab_score + 1 >= 0:
                ba -= ab_score - 1
                ab_score = 1
            elif ba > 0:
                ab_score -= ba
                ba = 0
        a -= ab_score
        b -= ab_score
        # print("Calculating AB", ab_score, a, b, ab, ba)
    # print("After AB collection scored", a, b, ab, ba)
    for _, ba_score, _, _ in ba_collections:
        if ba - ba_score >= 0:
            ba -= ba_score
            ba_score = 0
        elif ba > 0:
            ba_score -= ba
            ba = 0
        if ba_score > 1:
            if ab - ba_score + 1 >= 0:
                ab -= ba_score - 1
                ba_score = 1
            elif ab > 0:
                ba_score -= ab
                ab = 0
        # print("Calculating BA", ba_score, a, b, ab, ba)
        a -= ba_score
        b -= ba_score
    for score, _, a_score, b_score in common_collections:
        a -= a_score
        b -= b_score
        if ab - score >= 0:
            ab -= score
            score = 0
        elif ab > 0:
            score -= ab
            ab = 0
        if ba - score >= 0:
            ba -= score
            score = 0
        elif ba > 0:
            score -= ba
            ba = 0
        a -= score
        b -= score

    debugPrint("Calculated", a, b, ab, ba)
    if a >= 0 and b >= 0:
        print("YES")
    else:
        print("NO")


# ----------------------------------------------------
T = int(input())
for t in range(T):
    debugPrint(f"Test Case #{t}:")
    case_solver()
