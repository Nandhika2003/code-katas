#!/usr/bin/env python3

import itertools
import json
import sys
sys.path.append("..")

from dataclasses import dataclass

from ansi import *
from comp import *

@dataclass
class Cube:
    xl: int
    xr: int
    yl: int
    yr: int
    zl: int
    zr: int

    def __eq__(self, other):
        return all(
            [
                self.xl == other.xl,
                self.xr == other.xr,
                self.yl == other.yl,
                self.yr == other.yr,
                self.zl == other.zl,
                self.zr == other.zr,
            ]
        )

def get_area(cube):
    return (cube.xr - cube.xl + 1) * (cube.yr - cube.yl + 1) * (cube.zr - cube.zl + 1)

def get_intersection(cube1, cube2):
    x_overlap = list(range(max(cube1.xl, cube2.xl), min(cube1.xr, cube2.xr) + 1))
    y_overlap = list(range(max(cube1.yl, cube2.yl), min(cube1.yr, cube2.yr) + 1))
    z_overlap = list(range(max(cube1.zl, cube2.zl), min(cube1.zr, cube2.zr) + 1))
    for product in itertools.product(x_overlap, y_overlap, z_overlap):
        yield product

def get_cubes(xl, xr, yl, yr, zl, zr):
    x_range = [i for i in range(xl, xr + 1)]
    y_range = [i for i in range(yl, yr + 1)]
    z_range = [i for i in range(zl, zr + 1)]
    for product in itertools.product(x_range, y_range, z_range):
        yield product

def valid_line(xl, xr, yl, yr, zl, zr, direction):
    if xl < -50 and xr < -50: return False
    if xl > +50 and xr > +50: return False
    if yl < -50 and yr < -50: return False
    if yl > +50 and yr > +50: return False
    if zl < -50 and zr < -50: return False
    if zl > +50 and zr > +50: return False
    return True

def solve(prob, inputname):
    lines = []
    gen = yield_line(inputname)

    for line in gen:
        lines.append(
            parse(
                r"(on|off) x=(-?\d+)\.\.(-?\d+),y=(-?\d+)\.\.(-?\d+),z=(-?\d+)\.\.(-?\d+)",
                line
            )
        )

    for i in range(len(lines)):
        operation = lines[i][0]
        lines[i] = list(map(int, lines[i][1:])) + [operation]

    if prob == 1:
        lines = [line for line in lines if valid_line(*line)]

    room = set()
    cubes = []

    """
    ON
        ON  - only increment by the new cubes (new_cube - intersection(new_cube, old_cube))
        OFF - decrement all

    OFF
        ON  - increment all
        OFF - only decrement by the new cubes (new_cube - intersection(new_cube, old_cube))
    """

    for line in lines:
        operation = line[-1]
        new_cube = Cube(line[0], line[1], line[2], line[3], line[4], line[5])
        for cube in cubes
        """
        if line[-1] == "on":
            for cube in cubes:
                room.add(cube)
        elif line[-1] == "off":
            for cube in cubes:
                room.discard(cube)
        """

    if prob == 1:
        return len(room)
    elif prob == 2:
        return 2
    else:
        print("Invalid problem code")
        exit()
