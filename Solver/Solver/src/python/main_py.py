import sys

import utils
import solution as solution

# import aoc.y2024.main_py_2024_12_2 as solution


# to run in Terminal: python3 src/python/main_py.py
# if output is to large: python3 src/python/main_py.py | less -R

#  Test Cases -----------------------------------------------------------------------


def testCase(i, expected=None):
    utils.testCase(i, expected, lambda i, input: solution.aoc_solver(i, input))


sys.setrecursionlimit(10**6)

with open("src/output/output.txt", "w+") as file:
    sys.stdout = utils.writer(sys.stdout, file)

    testCase(1)
    # testCase(2)
    # testCase(3)
    # testCase(4)
    # testCase(5)

    if hasattr(solution, "__YEAR__") and hasattr(solution, "__DAY__"):
        utils.download_content(solution.__YEAR__, solution.__DAY__)
        testCase("puzzle")
