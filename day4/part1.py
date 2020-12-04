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

def get_passport(kvs):
    d = {}
    for kv in kvs:
        k,v = kv.split(':')
        d[k] = v
    return d

def file_contents(filepath, strip_empty_lines=True):
    empty_lines = not strip_empty_lines
    with open(filepath, "r") as fh:
        lines = [l.strip() for l in fh if (empty_lines or l.strip())]
    return lines

def parse_passports(filepath):
    passports = []
    with open(filepath, "r") as fh:
        passport = []
        for l in fh:
            line = l.strip()
            if line:
                passport.extend(line.split(' '))
            else:
                passports.append(get_passport(passport))
                passport = []
        if passport:
            passports.append(get_passport(passport))
    return passports


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
    passports = parse_passports(args.file)

    valid = 0
    for p in passports:
        ks = set(p.keys())
        if 'cid' in ks:
            ks.remove('cid')
        if len(ks) == 7:
            valid += 1

    print(f"There are {valid} valid passports")

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help='Input file, default: {}'.format(DEFAULT_INPUT_FILE), default=DEFAULT_INPUT_FILE, required=True)
    parser.add_argument('-v', '--verbose', help="Verbose output", default=False, action="store_true")
    args = parser.parse_args()

    main(args)