
import collections
from queue import Queue
from collections import deque
import fileinput, re

file_path = "input.txt"

with open(file_path, 'r') as file:
    lines = file.readlines()

#lines = [n.strip() for n in lines]

