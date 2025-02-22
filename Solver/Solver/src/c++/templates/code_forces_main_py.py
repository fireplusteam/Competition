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


if len(sys.argv) > 1 and sys.argv[1] == "DEBUG":
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

    def primary_reduce(val, score):
        if val - score >= 0:
            return (val - score, 0)
        else:
            return (0, score - val)

    def secondary_reduce(val, score):
        if score > 1:
            if val - score + 1 >= 0:
                return (val - score + 1, 1)
            else:
                return (0, score - val)
        return (val, score)

    for ab_score, _, _, _ in ab_collections:
        ab, ab_score = primary_reduce(ab, ab_score)
        ba, ab_score = secondary_reduce(ba, ab_score)
        a -= ab_score
        b -= ab_score
    for _, ba_score, _, _ in ba_collections:
        ba, ba_score = primary_reduce(ba, ba_score)
        ab, ba_score = secondary_reduce(ab, ba_score)
        a -= ba_score
        b -= ba_score
    for score, _, a_score, b_score in common_collections:
        a -= a_score
        b -= b_score
        ab, score = primary_reduce(ab, score)
        ba, score = primary_reduce(ba, score)
        a -= score
        b -= score

    if a >= 0 and b >= 0:
        print("YES")
    else:
        print("NO")


# ----------------------------------------------------
T = int(input())
for t in range(T):
    debugPrint(f"Test Case #{t}:")
    case_solver()
