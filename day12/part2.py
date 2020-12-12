#!/usr/bin/env python

"""
Advent of Code 2020
bad answers:
45283
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
DEFAULT_WAYPOINT_X = 10
DEFAULT_WAYPOINT_Y = 1

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

def rotate_waypoint(waypoint_x, waypoint_y, instruction, value):
    ticks = int(value/90)
    print(f"({waypoint_x},{waypoint_y}), {instruction}, {value}, {ticks=}")
    if ticks == 2:
        # rotate 180 degrees
        return (waypoint_x * -1, waypoint_y * -1)

    # going 270 degrees is like 90 in the opposite direction
    d = instruction
    if ticks == 3:
        ticks = 1
        d = Direction.LEFT if instruction == Direction.RIGHT else Direction.RIGHT

    new_x = waypoint_y * -1 if d == Direction.LEFT else waypoint_y
    new_y = waypoint_x * -1 if d == Direction.RIGHT else waypoint_x
    print(f"Given, {d}, {new_x=},{new_y=}")
    return (new_x, new_y)

def main(args):
    things = parse_file(args.file)

    current_heading = Direction[args.heading]
    waypoint_x = args.waypoint_x
    waypoint_y = args.waypoint_y
    x = 0
    y = 0

    for instruction, value in things:
        print(f"ship({x},{y}), waypoint({waypoint_x},{waypoint_y}), {instruction}, {value}")
        if instruction.isRotation():
            waypoint_x, waypoint_y = rotate_waypoint(waypoint_x, waypoint_y, instruction, value)
            print(f"Rotate: waypoint({waypoint_x},{waypoint_y})")
        elif instruction == Direction.FORWARD:
            x += waypoint_x * value
            y += waypoint_y * value
            print(f"Forward: {x},{y}")
        elif instruction == Direction.NORTH:
            waypoint_y += value
        elif instruction == Direction.EAST:
            waypoint_x += value
        elif instruction == Direction.SOUTH:
            waypoint_y -= value
        elif instruction == Direction.WEST:
            waypoint_x -= value

    m_dist = manhattan_distance(x, y)
    print(f"{m_dist=}")


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help='Input file, default: {}'.format(DEFAULT_INPUT_FILE), default=DEFAULT_INPUT_FILE, required=True)
    parser.add_argument('-v', '--verbose', help="Verbose output", default=False, action="store_true")
    parser.add_argument('-H', '--heading', help=f"Heading, default={DEFAULT_HEADING}", choices=['NORTH','SOUTH','EAST','WEST'], default=DEFAULT_HEADING)
    parser.add_argument('-x', '--waypoint_x', type=int, help=f"Waypoint X, default: {DEFAULT_WAYPOINT_X}", default=DEFAULT_WAYPOINT_X)
    parser.add_argument('-y', '--waypoint_y', type=int, help=f"Waypoint Y, default: {DEFAULT_WAYPOINT_Y}", default=DEFAULT_WAYPOINT_Y)
    args = parser.parse_args()

    main(args)