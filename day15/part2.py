#!/usr/bin/env python

"""
Advent of Code 2020

bad answers:
328169
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

def file_contents(filepath, strip_empty_lines=True):
    empty_lines = not strip_empty_lines
    with open(filepath, "r") as fh:
        lines = [l.strip() for l in fh if (empty_lines or l.strip())]
    return lines


def main(args):
    things = list(map(int, file_contents(args.file)[0].split(',')))

    turn = 1
    spoken = dict()
    last_num = next_num = None
    while turn != 30000001:
        if things:
            next_num = things.pop(0)
        elif last_num not in spoken or len(spoken[last_num]) == 1:
            next_num = 0
        else:
            next_num = spoken[last_num][-1] - spoken[last_num][-2]

        if next_num not in spoken:
            spoken[next_num] = []

        # store junk
        spoken[next_num].append(turn)
        if len(spoken[next_num]) > 2:
            spoken[next_num].pop(0)
        turn += 1

        last_num = next_num

    print(f"After turn {turn}, the last number spoken was {last_num}")

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help='Input file, default: {}'.format(DEFAULT_INPUT_FILE), default=DEFAULT_INPUT_FILE, required=True)
    parser.add_argument('-v', '--verbose', help="Verbose output", default=False, action="store_true")
    args = parser.parse_args()

    main(args)