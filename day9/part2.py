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
DEFAULT_TARGET = 675280050


def file_contents(filepath, strip_empty_lines=True):
    empty_lines = not strip_empty_lines
    with open(filepath, "r") as fh:
        lines = [l.strip() for l in fh if (empty_lines or l.strip())]
    return lines

def sum_until_equal_or_greater(target, numbers, start_index, start_sum):
    running_sum = start_sum
    for i in range(start_index, len(numbers)):
        running_sum += numbers[i]
        if running_sum >= target:
            return (running_sum - target, i)

def main(args):
    numbers = list(map(int, file_contents(args.file)))

    target_sum = args.target
    test_sum = 0
    for i,n in enumerate(numbers):
        test_sum += n
        finding, last_index = sum_until_equal_or_greater(target_sum, numbers, start_index=i+1, start_sum=test_sum)
        if finding > 0:
            test_sum -= n
            continue
        else:
            n_min = min(numbers[i:last_index+1])
            n_max = max(numbers[i:last_index+1])
            total = n_min + n_max
            print(f"{finding=}, [{i=}:{last_index+1}], {n_min=}, {n_max=}, {total=}")
            break

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help='Input file, default: {}'.format(DEFAULT_INPUT_FILE), default=DEFAULT_INPUT_FILE, required=True)
    parser.add_argument('-v', '--verbose', help="Verbose output", default=False, action="store_true")
    parser.add_argument('-t', '--target', help=f"Target, default: {DEFAULT_TARGET}", type=int, default=DEFAULT_TARGET)
    args = parser.parse_args()

    main(args)