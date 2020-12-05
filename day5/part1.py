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

LOW_HIGH_MAP = dict(
    F = 0,
    L = 0,
    B = 1,
    R = 1
)

class Seat(object):
    def __init__(self, s):
        self.s = s
        self.row = None
        self.col = None
        self.set_position()

    @property
    def id(self):
        return self.row * 8 + self.col
    
    def set_position(self):
        row_orders = self.s[:7]
        col_orders = self.s[-3:]
        self.row = Seat.find_position(row_orders, 0, 127)
        self.col = Seat.find_position(col_orders, 0, 7)

    @staticmethod
    def find_position(items, low, high):
        for i in items:
            new_low, new_high = Seat.refine_nums(low, high, LOW_HIGH_MAP[i])
            print(f"refine_nums({low}, {high}, {i}) = {new_low}, {new_high}")
            low = new_low
            high = new_high

        assert low == high
        return low

    @staticmethod
    def refine_nums(low, high, is_high):
        items = high - low + 1
        half = int(items/2)
        if is_high:
            return (low + half, high)
        else:
            return (low, low + half - 1)


def parse_seats(filepath):
    with open(filepath, "r") as fh:
        seats = [Seat(l.strip()) for l in fh]
    return seats


def main(args):
    seats = parse_seats(args.file)
    highest = max([s.id for s in seats])
    print(f"The highest ID is {highest}")

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help='Input file, default: {}'.format(DEFAULT_INPUT_FILE), default=DEFAULT_INPUT_FILE, required=True)
    parser.add_argument('-v', '--verbose', help="Verbose output", default=False, action="store_true")
    args = parser.parse_args()

    main(args)