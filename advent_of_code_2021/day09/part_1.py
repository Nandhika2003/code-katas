#!/usr/bin/env python3

import sys
import math

from math import gcd, floor, sqrt, log
from collections import defaultdict, deque
from bisect import bisect_left, bisect_right

inputname = "example"
inputname = "real"

_lines = open(inputname, "r").read().splitlines()
lines = [list(map(int, row)) for row in _lines]

MOVES = ((-1, 0), (0, -1), (0, 1), (1, 0))

def is_low_point(point, x, y, rows, cols):
    for MOVE in MOVES:
        new_x = x + MOVE[0]
        new_y = y + MOVE[1]
        if new_x >= 0 and new_x < rows and new_y >= 0 and new_y < cols:
            if point[x][y] >= point[new_x][new_y]:
                return False
    return True

def get_risk(point, x, y):
    return point[x][y] + 1

risk_sum = 0

for i in range(len(lines)):
    for j in range(len(lines[i])):
        if is_low_point(lines, i, j, len(lines), len(lines[0])):
            risk_sum += get_risk(lines, i, j)

print(risk_sum)
