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

# class Color(Enum):
#     RED = 0
#     GREEN = 1
#     BLUE = 2

@dataclass
class Tile:
    x: int
    y: int


def file_contents(filepath, strip_empty_lines=True):
    empty_lines = not strip_empty_lines
    with open(filepath, "r") as fh:
        lines = [l.strip() for l in fh if (empty_lines or l.strip())]
    return lines


def parse_file(filepath):
    lines = file_contents(filepath)
    things = []
    for line in lines:

        # Parse with split
        bits = line.split(',')
        things.append(Tile(*bits))

        # Parse with regex
        # mobj = re.match(r'', line)
        # if mobj:
        #     print(mobj)

    return things


def main(args):
    target = 2020
    things = list(map(int, file_contents(args.file)))

    # Brute force, nasty but works
    for i,x in enumerate(things):
        for j,y in enumerate(things):
            for k,z in enumerate(things):
                if i != j and i != k and j != k and x+ y + z == target:
                    print(f"{x} * {y} * {z} = {x*y*z}")
                    exit(0)

    print("Uh oh")


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help='Input file, default: {}'.format(DEFAULT_INPUT_FILE), default=DEFAULT_INPUT_FILE, required=True)
    parser.add_argument('-v', '--verbose', help="Verbose output", default=False, action="store_true")
    args = parser.parse_args()

    main(args)