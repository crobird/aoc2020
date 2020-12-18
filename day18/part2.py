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

def process_add_regex(rx):
    print(f"process_add_regex: {rx.group(1)=} {rx.group(2)=} {rx.group(3)=} {rx.group(4)=}")
    return rx.group(1) + str(int(rx.group(2)) + int(rx.group(3))) + rx.group(4)

def process_mult_regex(rx):
    print(f"process_mult_regex: {rx.group(1)=} {rx.group(2)=} {rx.group(3)=} {rx.group(4)=}")
    a = int(rx.group(2))
    b = int(rx.group(3))
    print(f"{a} * {b} = {a*b}")
    return rx.group(1) + str(int(rx.group(2)) * int(rx.group(3))) + rx.group(4)

def process_simple_eq(s):
    while s.find('+') != -1:
        s = re.sub(r'(.*?)(\d+)\s*\+\s*(\d+)(.*)', process_add_regex, s)
        print(f"{s=}")

    while s.find('*') != -1:
        s = re.sub(r'(.*?)(\d+)\s*\*\s*(\d+)(.*)', process_mult_regex, s)
        print(f"{s=}")

    return int(s)

def process_simple_regex_eq(rx):
    print(f"process_simple_regex_eq: {rx.group(1)} || {rx.group(2)} || {rx.group(3)}")
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