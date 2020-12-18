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

def process_op(a, b, op):
    if op == '+':
        a += b
    elif op == '*':
        a *= b
    else:
        raise Exception("Should never get here, bro")
    return a

def process_simple_eq(s):
    print(f"{s=}")
    total = 0
    last_op = '+'
    last_digit = ''
    for c in s:
        if c.isdigit():
            last_digit += c
        elif c == ' ':
            continue
        elif c in ['+', '*']:
            last_int = int(last_digit)
            total = process_op(total, last_int, last_op)
            last_op = c
            last_digit = ''
    last_int = int(last_digit)
    return process_op(total, last_int, last_op)

def process_simple_regex_eq(rx):
    print(f"{rx.group(1)} || {rx.group(2)} || {rx.group(3)}")
    return rx.group(1) + str(process_simple_eq(rx.group(2))) + rx.group(3)

def calculate_thing(t):
    # Reduce our groups
    while t.find('(') != -1:
        t = re.sub(r'(.*)\(([^\(\)]+)\)(.*)', process_simple_regex_eq , t)
        print(f"{t=}")

    return process_simple_eq(t)

def main(args):
    things = file_contents(args.file)

    v_sum = 0
    for t in things:
        v_sum += calculate_thing(t)
    print(f"The sum of all the things is {v_sum}")


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help='Input file, default: {}'.format(DEFAULT_INPUT_FILE), default=DEFAULT_INPUT_FILE, required=True)
    parser.add_argument('-v', '--verbose', help="Verbose output", default=False, action="store_true")
    args = parser.parse_args()

    main(args)