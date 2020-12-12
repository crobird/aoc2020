#!/usr/bin/env python

"""
Advent of Code 2020
"""

import os
import re
import math
import collections
from enum import Enum
from dataclasses import dataclass

me = os.path.basename(__file__)

DEFAULT_INPUT_FILE = "input/" + me.replace(".py", ".txt")
DEFAULT_HEADING = 'EAST'

class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3
    LEFT = 4
    RIGHT = 5
    FORWARD = 6
    N = 0
    E = 1
    S = 2
    W = 3
    L = 4
    R = 5
    F = 6

    def isRotation(self):
        return self.value in [Direction.RIGHT.value, Direction.LEFT.value]



def file_contents(filepath, strip_empty_lines=True):
    empty_lines = not strip_empty_lines
    with open(filepath, "r") as fh:
        lines = [l.strip() for l in fh if (empty_lines or l.strip())]
    return lines


def parse_file(filepath):
    lines = file_contents(filepath)
    things = []
    for line in lines:
        # Parse with regex
        mobj = re.match(r'(\w)(\d+)', line)
        if mobj:
            things.append((Direction[mobj.group(1)], int(mobj.group(2))))
    return things

def rotate(current, instruction, value):
    x = int(value/90)
    if instruction == Direction.LEFT:
        x = (x + 4) * -1
    new_index = (current.value + x) % 4
    return Direction(new_index)

def manhattan_distance(x, y):
    return abs(x) + abs(y)

def main(args):
    things = parse_file(args.file)

    current_heading = Direction[args.heading]
    x = 0
    y = 0

    for instruction, value in things:
        if instruction.isRotation():
            current_heading = rotate(current_heading, instruction, value)
            continue

        move_direction = current_heading if instruction == Direction.FORWARD else instruction

        if move_direction == Direction.NORTH:
            y += value
        elif move_direction == Direction.EAST:
            x += value
        elif move_direction == Direction.SOUTH:
            y -= value
        elif move_direction == Direction.WEST:
            x -= value

    m_dist = manhattan_distance(x, y)
    print(f"{m_dist=}")


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help='Input file, default: {}'.format(DEFAULT_INPUT_FILE), default=DEFAULT_INPUT_FILE, required=True)
    parser.add_argument('-v', '--verbose', help="Verbose output", default=False, action="store_true")
    parser.add_argument('-H', '--heading', help=f"Heading, default={DEFAULT_HEADING}", choices=['NORTH','SOUTH','EAST','WEST'], default=DEFAULT_HEADING)
    args = parser.parse_args()

    main(args)