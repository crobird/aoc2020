#!/usr/bin/env python

"""
Advent of Code 2020

bad answers:
    5005670400
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

def check_trees(hill, x_mod, y_mod):
    x = x_mod
    y = y_mod

    tree_count = 0
    while y < len(hill):
        local_x = x
        if local_x >= len(hill[y]):
            local_x = local_x % len(hill[y])

        value = hill[y][local_x]
        if value == '#':
            newval = 'X'
            tree_count += 1
        else:
            newval = 'O'

        x += x_mod
        y += y_mod

    return tree_count



def main(args):
    things = file_contents(args.file)
    
    slopes = [ (1,1), (3,1), (5,1), (7,1), (1,2) ]
    tree_counts = [check_trees(things, *x) for x in slopes]

    x = 1
    for n in tree_counts:
        x *= n

    print(x)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help='Input file, default: {}'.format(DEFAULT_INPUT_FILE), default=DEFAULT_INPUT_FILE, required=True)
    parser.add_argument('-v', '--verbose', help="Verbose output", default=False, action="store_true")
    args = parser.parse_args()

    main(args)