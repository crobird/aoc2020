#!/usr/bin/env python

"""
Advent of Code 2020
"""

import os
import re
import math
import collections
from copy import deepcopy
from enum import Enum
from dataclasses import dataclass

me = os.path.basename(__file__)

DEFAULT_INPUT_FILE = "input/" + me.replace(".py", ".txt")

class Seat(Enum):
    OCCUPIED = 0
    EMPTY = 1
    FLOOR = 2

    def __str__(self):
        if self.value == Seat.OCCUPIED.value:
            return '#'
        elif self.value == Seat.EMPTY.value:
            return 'L'
        elif self.value == Seat.FLOOR.value:
            return '.'

    def fromChar(c):
        if c == '#':
            return Seat.OCCUPIED
        elif c == 'L':
            return Seat.EMPTY
        elif c == '.':
            return Seat.FLOOR
        else:
            raise Exception(f"Unexpected value given: {c}")


# class Color(Enum):
#     RED = 0
#     GREEN = 1
#     BLUE = 2

@dataclass
class Tile:
    x: int
    y: int

def print_layout(layout, title=None):
    if title:
        print(f'\n-- {title} --')
    for row in layout:
        print(''.join(map(str, row)))

def parse_layout(filepath):
    layout = []
    with open(filepath, "r") as fh:
        for l in fh:
            line = l.strip()
            if not line:
                continue
            layout.append([Seat.fromChar(c) for c in line])
    return layout

def is_out_of_bounds(layout, x, y):
    return y < 0 or y >= len(layout) or x < 0 or x >= len(layout[0])

def occupied_neighbors(layout, x, y):
    taken = 0
    for i in range(y-1, y+2):
        for j in range(x-1, x+2):
            if (j == x and i == y) or is_out_of_bounds(layout, j, i):
                continue
            if layout[i][j] == Seat.OCCUPIED:
                taken += 1
    return taken

def seat_change(layout, x, y):
    seat = layout[y][x]
    taken_nearby = occupied_neighbors(layout, x, y)
    if seat == Seat.EMPTY and not taken_nearby:
        return Seat.OCCUPIED
    elif seat == Seat.OCCUPIED and taken_nearby >= 4:
        return Seat.EMPTY
    return seat

def reseat(layout):
    new_layout = deepcopy(layout)
    for i in range(len(layout)):
        for j in range(len(layout[0])):
            new_layout[i][j] = seat_change(layout, j, i)
    return new_layout

def seat_em(layout):
    last_layout = layout
    next_layout = None
    count = 0
    next_layout = reseat(last_layout)
    while next_layout != last_layout:
        count += 1
        last_layout = next_layout
        next_layout = reseat(last_layout)
    return next_layout

def count_taken_seats(layout):
    count = 0
    for r in layout:
        count += r.count(Seat.OCCUPIED)
    return count


def main(args):
    layout = parse_layout(args.file)

    final_layout = seat_em(layout)
    taken_seats = count_taken_seats(final_layout)

    print(f"Number of taken seats in final layout: {taken_seats}")

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help='Input file, default: {}'.format(DEFAULT_INPUT_FILE), default=DEFAULT_INPUT_FILE, required=True)
    parser.add_argument('-v', '--verbose', help="Verbose output", default=False, action="store_true")
    args = parser.parse_args()

    main(args)