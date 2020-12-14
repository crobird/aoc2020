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

class Mask:
    def __init__(self, bitmask):
        self.bitmask = bitmask
        self.masks = dict()
        self.assign_masks()

    def __repr__(self):
        return f"Mask({self.bitmask}, {self.masks})"

    def assign_masks(self):
        for i,c in enumerate(self.bitmask):
            if c == 'X':
                continue
            self.masks[i] = c

    def mask_val(self, i):
        print(f"mask_val called on {i}")
        s = bin(i)[2:].zfill(36)
        new_s = []
        print(f"Masking: {s}")
        print(f"   with: {self.bitmask}")
        for i,c in enumerate(s):
            if i in self.masks:
                new_s.append(self.masks[i])
            else:
                new_s.append(c)
        s = '0b' + ''.join(new_s)
        new_i = int(s, 2)
        print(f"New i from {s} = {new_i}")
        return int(s, 2)

@dataclass
class Mem:
    slot: int
    val: int


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
        mobj = re.match(r'mask = ([01X]+)$', line)
        if mobj:
            things.append(Mask(mobj.group(1)))
            continue

        mobj = re.match(r'mem\[(\d+)\] = (\d+)$', line)
        if mobj:
            things.append(Mem(int(mobj.group(1)), int(mobj.group(2))))

    return things


def main(args):
    things = parse_file(args.file)

    storage = dict()

    latest_mask = None
    for t in things:
        if isinstance(t, Mask):
            print(f"Storing new Mask: {t}")
            latest_mask = t
        elif isinstance(t, Mem):
            print(f"Storing new Mem: {t}")
            storage[t.slot] = latest_mask.mask_val(t.val)

    total = sum(storage[k] for k in storage)
    print(f"{total=}")


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help='Input file, default: {}'.format(DEFAULT_INPUT_FILE), default=DEFAULT_INPUT_FILE, required=True)
    parser.add_argument('-v', '--verbose', help="Verbose output", default=False, action="store_true")
    args = parser.parse_args()

    main(args)