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


def file_contents(filepath, strip_empty_lines=True):
    empty_lines = not strip_empty_lines
    with open(filepath, "r") as fh:
        lines = [l.strip() for l in fh if (empty_lines or l.strip())]
    return lines


def main(args):
    things = list(map(int, file_contents(args.file)))
    things.sort()

    curr = 0
    diff_1 = 0
    diff_3 = 1 # counting the built-in adapter that's always +3
    for i,jolts in enumerate(things):
        diff = jolts - curr
        if diff == 1:
            diff_1 += 1
        elif diff == 3:
            diff_3 += 1
        else:
            print(f"You clearly don't understand how this works. ({diff=})")
        curr = jolts
    print(f"{diff_1=}*{diff_3=} = {diff_1*diff_3}")


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help='Input file, default: {}'.format(DEFAULT_INPUT_FILE), default=DEFAULT_INPUT_FILE, required=True)
    parser.add_argument('-v', '--verbose', help="Verbose output", default=False, action="store_true")
    args = parser.parse_args()

    main(args)