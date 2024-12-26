import sys

import utils

import solution as solution

# import aoc.y2024.main_py_2024_23_2 as solution


# to run in Terminal: python3 src/python/tests_runner.py
# if output is to large: python3 src/python/tests_runner.py | less -R

#  Test Cases -----------------------------------------------------------------------


def testCase(i, expected=None):
    task_i = str(i)
    if hasattr(solution, "__TASK_ID__") and len(solution.__TASK_ID__) > 0:
        task_i = solution.__TASK_ID__ + "_" + task_i
    utils.testCase(task_i, expected, lambda i: solution.aoc_solver(i))


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
