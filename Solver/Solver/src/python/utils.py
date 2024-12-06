import os
import sys
import time

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

def testCase(i, solver):
    print("----------------------------------------------")
    print(f"Test Case #{i}:")

    if not (input:=get_input(i)):
        print(f"  #{i} Skipped")
        return
    import time
    st = time.time()
    ans = solver(i, input)
    print(f"  #{i} Answer = {ans}")
    print(f"  #{i} Time = {time.time() - st: .5f}s")


# ------------------------------------ download input script
# python3 src/python/helper/get_input.py --year=2024 --day=3 > src/input/input_puzzle.txt
import subprocess
import os
def download_content(__YEAR__, __DAY__):
    cache_path = "src/python/helper/cache.txt"
    mode = "w+" if not os.path.exists(cache_path) else "r"
    with open(cache_path, mode) as file:
        is_downloaded = file.read()
    with open(cache_path, "w+") as file:
        identity = f"Year:{__YEAR__},Day:{__DAY__}"
        if is_downloaded != identity:
            process = subprocess.run(["python3", f"src/python/helper/get_input.py", f"--year={__YEAR__}", f"--day={__DAY__}"], stdout=subprocess.PIPE)
            with open("src/input/input_puzzle.txt", "wb+") as puzzle:
                if not b"Please don't repeatedly request this endpoint" in process.stdout:
                    puzzle.write(process.stdout)
                    file.write(identity)
                else:
                    file.write("")
                    puzzle.write(b"")
        else:
            file.write(identity)