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

@dataclass
class Operation:
    instruction: str
    sign: str
    number: int
    count: int = 0

    def reset(self):
        self.count = 0

def file_contents(filepath, strip_empty_lines=True):
    empty_lines = not strip_empty_lines
    with open(filepath, "r") as fh:
        lines = [l.strip() for l in fh if (empty_lines or l.strip())]
    return lines


def parse_file(filepath):
    lines = file_contents(filepath)
    instructions = []
    for line in lines:
        # Parse with regex
        mobj = re.match(r'(\w+)\s([\-+])(\d+)$', line)
        if not mobj:
            print(f"Bad news on the file parsing side, this didn't parse: {line}")
            exit(1)
        instructions.append(Operation(mobj.group(1), mobj.group(2), int(mobj.group(3)), 0))

    return instructions

def run_instructions(instructions, reset_counts=False):
    if reset_counts:
        for i in instructions:
            i.reset()

    ptr = 0
    val = 0
    err = 0
    while True:
        next_ptr = 1
        if ptr == len(instructions):
            break
        x = instructions[ptr]
        if x.count:
            err = 1
            break
        x.count += 1
        offset = x.number if x.sign == '+' else x.number * -1
        if x.instruction == 'acc':
            val += offset
        elif x.instruction == 'jmp':
            next_ptr = offset
        ptr += next_ptr
    return (val, err)


def main(args):
    instructions = parse_file(args.file)

    for i in range(len(instructions)):
        x = instructions[i]
        if x.instruction == 'acc':
            continue
        orig = x.instruction
        opposite = 'jmp' if orig == 'nop' else 'nop'
        x.instruction = opposite
        val, err = run_instructions(instructions, reset_counts=True)
        if not err:
            print(f"Finished without error: {val=}, {i=}, {x=}")
            break
        x.instruction = orig


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help='Input file, default: {}'.format(DEFAULT_INPUT_FILE), default=DEFAULT_INPUT_FILE, required=True)
    parser.add_argument('-v', '--verbose', help="Verbose output", default=False, action="store_true")
    args = parser.parse_args()

    main(args)