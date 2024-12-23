import functools
from pathlib import Path
import re
import subprocess
import os
import sys
from collections.abc import Callable, Iterable
import heapq
from typing import Literal


class HeapObj(object):
    def __init__(self, val, min=True, key: Callable | None = None):
        self.val = val
        self.key = key
        self.min = min

    def __lt__(self, other):
        if self.key is not None:
            if self.min:
                return self.key(self.val) < self.key(other.val)
            return self.key(self.val) > self.key(other.val)
        if self.min:
            return self.val < other.val
        return self.val > other.val

    def __eq__(self, other):
        if self.key is not None:
            return self.key(self.val) == self.key(other.val)
        return self.val == other.val

    def __str__(self):
        return str(self.val)


class MinHeap(object):
    def __init__(self, array: Iterable | None, key: Callable | None = None):
        self.h = []
        self.key = key
        if array is None:
            return
        for i in array:
            self.put(i)

    def put(self, x):
        if self.key is not None:
            x = HeapObj(x, min=True, key=self.key)
        heapq.heappush(self.h, x)

    def get(self):
        val = heapq.heappop(self.h)
        if isinstance(val, HeapObj):
            return val.val
        return val

    def __getitem__(self, i):
        return self.h[i]

    def __len__(self):
        return len(self.h)


global_recursive_depth = 0


def recursive_indent(indent):
    return " |" * (indent)


def printRec(
    *values: object,
    sep: str | None = " ",
    end: str | None = "\n",
    file=None,
    flush: Literal[False] = False,
):
    should_print_indent = True
    for t, value in enumerate(values):

        def print_sep():
            nonlocal should_print_indent
            if should_print_indent:
                print(indent, end=str_separator)
                should_print_indent = False

        indent = recursive_indent(global_recursive_depth)
        str_separator = "" if len(indent) == 0 else " "

        if isinstance(value, str):  # multiline
            value = value.split("\n")
            for i, r in enumerate(value):
                print_sep()
                print(r, end="", file=file, flush=flush)
                if i != len(value) - 1:
                    print("\n", end="")
                    should_print_indent = True
        else:
            print_sep()
            print(value, end="", file=file, flush=flush)
        if t != len(values) - 1:
            print(sep, end="")
            if "\n" in sep:
                should_print_indent = True
    print("", end=end)


def trace_recursive_calls(func):
    """
    trace recursive function with calls and returns
    use like
    @utils.trace_recursive_calls
    def rec_func(...):
        pass
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        global global_recursive_depth
        nonlocal current_depth
        indent = recursive_indent(global_recursive_depth + 1)
        print(f"{indent[:-1]}{func.__name__} called: ({', '.join(str(arg) for arg in args)})" + " {")
        global_recursive_depth += 1
        current_depth += 1
        result = func(*args, **kwargs)
        global_recursive_depth -= 1
        current_depth -= 1
        print(f"{indent[:-1]}{func.__name__}({', '.join(str(arg) for arg in args)}) returning {result}" + " }")
        return result

    current_depth = 0
    return wrapper


class MaxHeap(MinHeap):
    def put(self, x):
        heapq.heappush(self.h, HeapObj(x, min=False, key=self.key))

    def get(self):
        return heapq.heappop(self.h).val

    def __getitem__(self, i):
        return self.h[i].val


def FourD(rows, columns, z, w, def_val):
    """
    Create array of 4 dimensions like this
    array[rows][columns][z][w]
    """
    return [[[[def_val for _ in range(w)] for _ in range(z)] for _ in range(columns)] for _ in range(rows)]


def ThreeD(rows, columns, z, def_val):
    """
    Create array of 3 dimensions like this
    array[rows][columns][z]
    """
    return [[[def_val for _ in range(z)] for _ in range(columns)] for _ in range(rows)]


def TwoD(rows, columns, def_val):
    """
    Create array of 2 dimensions like this
    array[rows][columns]
    """
    return [[def_val for _ in range(columns)] for _ in range(rows)]


def to_deep_tuple(*keys):
    """
    used to convert any list/dict/set based tree object to not mutable tuple which can used as a key in set of dict
    used for complex data structures. It's slower but guarantee that the entire object of dict/set/list is hashed
    """

    def to_key(key):
        if isinstance(key, str):
            return key
        if isinstance(key, Iterable):
            if isinstance(key, dict):
                l = [(to_key(k), to_deep_tuple(v)) for k, v in key.items()]
            else:
                l = [to_key(x) for x in key]
            if isinstance(key, set):  # unordered set
                l.sort()
            return tuple(l)
        else:
            return str(key)

    return tuple([to_key(key) for key in keys])


def to_deep_hash(*key):
    """
    Return a hash of all object in the tree
    used for complex data structures
    """
    return hash(to_deep_tuple(*key))


def split_by_strings(delimiters: list[str], string: str):
    """
    split input string by multiple delimiters regexp like
    'Some: +10, 10: works like 20'
    split_by_strings([r"Some: \\+", r",", r": work like "])
    returns 10 10 10
    and trim all empty results
    """
    if isinstance(delimiters, str):
        pattern = re.compile(delimiters)
    else:
        pattern = re.compile("|".join(delimiters))
    l = [x for x in re.split(pattern, string) if len(x) > 0]
    return l


def print_to_string(*args, **kwargs):
    import io

    output = io.StringIO()
    print(*args, file=output, **kwargs)
    contents = output.getvalue()[:-1]
    output.close()
    return contents


def debugPrint(*args, recursive=True, **kwargs):
    """
    Print list of string or list of list of string by concatenating it to grid
    l"123131" -> list like ["1", "2", "3", ...]
    t"123131" -> tuple like ("1", "2", "3", ...)
    """

    def indent(rec):
        return "  ".join(["" for x in range(rec + 1)])

    def empty(rec):
        return " ".join(["" for x in range(rec + 1)])

    def startWithBracket(line):
        for i in line:
            if i == "{":
                return True
            if i == "\n":
                return False
        return False

    def maxColumns(x):
        maxWidth = 0
        currentWidth = 0
        for i in x:
            if i == "\n":
                currentWidth = 0
            else:
                currentWidth += 1
                maxWidth = max(maxWidth, currentWidth)
        return min(2, maxWidth)

    def dbPrint(field, rec_depth):
        if isinstance(field, dict):
            l = [(print_to_string(dbPrint(k, rec_depth + 1)), print_to_string(dbPrint(v, rec_depth + 1))) for k, v in field.items()]
            r = []
            for x, y in l:
                a = x
                b = y
                if not (x.find("\n") == -1):
                    middle = ("\n" + indent(rec_depth + 1)).join(x.split("\n"))
                    a = f"\n{indent(rec_depth + 1)
                             }{middle}"
                if not (y.find("\n") == -1 or startWithBracket(y)):
                    middle = ("\n" + indent(rec_depth + 1) + empty(maxColumns(x))).join(y.split("\n"))
                    b = f"\n{indent(rec_depth + 1)
                             }{empty(maxColumns(x))}{middle}"
                r.append((a, b))
            l = [f"{x}: {y}" for x, y in r]
            sep = f",\n{indent(rec_depth + 1)}"
            return "{\n" + indent(rec_depth + 1) + f"{sep.join(l)}" + "\n" + indent(rec_depth) + "}"
        elif isinstance(field, list) or isinstance(field, tuple):
            # flatten
            if len(field) > 0 and isinstance(field[0], str) and len(field[0]) == 1:
                return f'{"l" if isinstance(field, list) else "t"}"' + "".join(field) + '"'
            elif (
                len(list(field)) > 0
                and (isinstance(field[0], tuple) or isinstance(field[0], list) or isinstance(field[0], str))
                and isinstance(field[0][0], str)
                and len(field[0][0]) == 1
            ):  # grid
                l = [dbPrint(x, rec_depth) for x in field]
                return f"{"[" if isinstance(field, list) else "("}" + ",\n ".join(l) + ("]" if isinstance(field, list) else ")")
            else:
                r = [dbPrint(x, rec_depth) for x in field]
                r = [x if x.find("\n") == -1 or startWithBracket(x) else ("\n" + x) for x in r]

                r = ", ".join(r)
                if isinstance(field, list):
                    return "[" + r + "]"
                else:
                    return "(" + r + ")"
        elif isinstance(field, set):
            l = [print_to_string(dbPrint(k, rec_depth + 1)) for k in field]
            l = [y if y.find("\n") == -1 else f"{("\n" + indent(rec_depth + 1)).join(y.split("\n"))}" for y in l]
            sep = f",\n{indent(rec_depth + 1)}"
            return "{\n" + indent(rec_depth + 1) + f"{sep.join(l)}" + "\n" + indent(rec_depth) + "}"
        else:
            return print_to_string(field)

    if args:
        for field in args:
            if recursive:
                printRec(dbPrint(field, 0))
            else:
                print(dbPrint(field, 0))
    if kwargs:
        for k, field in kwargs.items():
            if recursive:
                printRec(f"{dbPrint(k), 0}:")
                printRec(dbPrint(field, 0))
            else:
                print(f"{dbPrint(k), 0}:")
                print(dbPrint(field, 0))


# Input Parser------------------------------------------------------------------------------------------------------


def get_input(i):
    file_path = f"src/input/input_{i}.txt"
    if not os.path.exists(file_path):
        return None
    with open(file_path, "r") as file:
        r = file.read()
        if len(r) == 0:
            return None
    return r


class Colors:
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"


class writer:
    """Used to write to file and stdout"""

    _max_megabytes = 32

    def __init__(self, *writers):
        self.writers = writers
        self.nums = 0
        self.threshold = self._max_megabytes * 1024 * 1024  # 8 mb
        self.should_write_truncation_message = True

    def write(self, text):
        def filter(text: str):
            if text.find(Colors.ENDC) != -1:
                return text.replace(Colors.ENDC, "").replace(Colors.OKGREEN, "").replace(Colors.WARNING, "").replace(Colors.FAIL, "")
            return text

        self.nums += len(text)

        should_print = self.nums < self.threshold or text.startswith(">")

        was_truncated = False
        for w in self.writers:
            if should_print:
                if self.nums >= self.threshold and text.startswith(">"):
                    w.write("\n")
                if hasattr(w, "name") and w.name != "<stdout>":
                    to_print = filter(text)
                    w.write(to_print)
                else:
                    w.write(text)
            elif self.should_write_truncation_message:
                w.write(f"\n......Output is truncated as it's more then {self._max_megabytes} mb\n")
                was_truncated = True
        if was_truncated:
            self.should_write_truncation_message = False
            should_print = True
        self._flush(should_print)

    def _flush(self, should_print, recursive=False):
        for w in self.writers:
            if hasattr(w, "closed") and not w.closed and hasattr(w, "_flush") and recursive:
                w._flush(should_print)
            if hasattr(w, "name") and w.name != "<stdout>":
                if should_print:
                    Path(w.name).touch()

    def flush(self):
        self._flush(True, True)


def testCase(i, expected, solver):

    saved = sys.stdout
    with open(f"src/output/output_{i}.txt", "w+") as file:
        sys.stdout = writer(sys.stdout, file)

        print(">----------------------------------------------")
        print(f"> Test Case #{i}:")

        if not (input := get_input(i)):
            print(f">  #{i} Skipped")
            sys.stdout = saved
            return
        import time

        st = time.time()
        ans = solver(i, input)
        if expected is not None:
            if print_to_string(expected) != print_to_string(ans):
                print(f">  {Colors.FAIL}#{i} Wrong Answer = {ans} 😡😡😡{Colors.ENDC}, Expected: {expected}")
            else:
                print(f">  {Colors.OKGREEN}#{i} Answer Correct = {ans} 🥳🥳🥳 {Colors.ENDC}")
        else:
            print(f">  {Colors.WARNING}#{i} Answer = {ans} 🤔🤔🤔, No expected answer Provided{Colors.ENDC}")
        print(f">  #{i} Time = {time.time() - st: .5f}s")
        sys.stdout = saved


# ------------------------------------ download input script
# python3 src/python/helper/get_input.py --year=2024 --day=3 > src/input/input_puzzle.txt


def download_content(__YEAR__, __DAY__):
    cache_path = "src/python/helper/cache.txt"
    mode = "w+" if not os.path.exists(cache_path) else "r"
    with open(cache_path, mode) as file:
        is_downloaded = file.read()
    with open(cache_path, "w+") as file:
        identity = f"Year:{__YEAR__},Day:{__DAY__}"
        if is_downloaded != identity:
            process = subprocess.run(
                [
                    "python3",
                    f"src/python/helper/get_input.py",
                    f"--year={
                                     __YEAR__}",
                    f"--day={__DAY__}",
                ],
                stdout=subprocess.PIPE,
            )
            with open("src/input/input_puzzle.txt", "wb+") as puzzle:
                if not b"Please don't repeatedly request this endpoint" in process.stdout:
                    puzzle.write(process.stdout)
                    file.write(identity)
                else:
                    file.write("")
                    puzzle.write(b"")
        else:
            file.write(identity)


if __name__ == "__main__":
    # Test Utils
    st = set(["s1", "s2"])
    dp = {
        "one": {
            "wow": 10,
            "second": {
                "third": ["o", "1", "2"],
                "list": ["01", "-2"],
                "forth": {"twoDims": [["1", "2"], ["3", "4"]], "tuple": ("1", "2")},
                "setKey": st,
                "multi\nline": "wow",
                ("10", "long key"): ("works\n"),
            },
            "tail": "tailed",
            tuple(st): ["set as a key", "ok"],
            "array": [[1, 2], [2, 3]],
            "experimental": ("exp1", ([("1", "2")]), "exp2"),
        }
    }
    debugPrint(dp)
