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
DEFAULT_PREAMBLE = 25


def file_contents(filepath, strip_empty_lines=True):
    empty_lines = not strip_empty_lines
    with open(filepath, "r") as fh:
        lines = [l.strip() for l in fh if (empty_lines or l.strip())]
    return lines

def is_valid_number(total, numbers, verbose=False):
    print(f"Checking for something that adds up to {total}")
    for i,n in enumerate(numbers):
        diff = total - n
        if i > 0:
            if diff in numbers[0:i]:
                if verbose:
                    print(f"Found {n} + {diff} = {total}")
                return True
        if i < len(numbers) - 1:
            if diff in numbers[i+1:]:
                if verbose:
                    print(f"Found {n} + {diff} = {total}")
                return True
    return False

def main(args):
    numbers = list(map(int, file_contents(args.file)))
    print(numbers)

    start_index = 0
    last_index = args.preamble - 1

    for i in range(args.preamble, len(numbers)):
        print(f"{i=}")
        if not is_valid_number(numbers[i], numbers[start_index:last_index+1], verbose=args.verbose):
            print(f"First invalid number is {numbers[i]}")
            break
        else:
            print(f"Found two numbers that matched: ")
        start_index += 1
        last_index += 1

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help='Input file, default: {}'.format(DEFAULT_INPUT_FILE), default=DEFAULT_INPUT_FILE, required=True)
    parser.add_argument('-v', '--verbose', help="Verbose output", default=False, action="store_true")
    parser.add_argument('-p', '--preamble', help=f"Preamble, default: {DEFAULT_PREAMBLE}", type=int, default=DEFAULT_PREAMBLE)
    args = parser.parse_args()

    main(args)