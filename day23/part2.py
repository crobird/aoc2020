#!/usr/bin/env python

"""
Advent of Code 2020
bad answers:
220171261611
"""

import os
import re
import math
import collections
from enum import Enum
from dataclasses import dataclass

me = os.path.basename(__file__)

DEFAULT_INPUT_FILE = "input/" + me.replace(".py", ".txt")
DEFAULT_MOVE_NUM = 10000000
DEFAULT_CUP_TAKE = 3
DEFAULT_CUP_NUM = 1000000

DEBUG_PRINT = False

class Cup:
    def __init__(self, val, prev=None, next=None):
        self.val = val
        self.prev = prev
        self.next = next

        if prev:
            prev.next = self

    @property
    def sval(self):
        return str(self.val)

def file_contents(filepath, strip_empty_lines=True):
    empty_lines = not strip_empty_lines
    with open(filepath, "r") as fh:
        lines = [l.strip() for l in fh if (empty_lines or l.strip())]
    return lines

def remove_cups(after_cup, n=DEFAULT_CUP_TAKE):
    removed = []
    c = after_cup
    for i in range(n):
        removed.append(c.next)
        c = c.next
    after_cup.next = removed[-1].next
    removed[-1].next.prev = after_cup
    return removed

def insert_cups(cups, after_cup):
    old_next = after_cup.next

    # Link in first cup
    after_cup.next = cups[0]
    cups[0].prev = after_cup

    # Link in last cup
    cups[-1].next = old_next
    old_next.prev = cups[-1]

def print_cups(current):
    s = f"({current.val})"
    c = current.next
    seen = { current.val: True }
    while c.val not in seen:
        s += " " + c.sval
        seen[c.val] = True
        c = c.next
    print(f"cups: {s}")

def take_turn(current, highest_val, cup_by_val, cup_take=DEFAULT_CUP_TAKE):
    print_cups(current) if DEBUG_PRINT else ""

    removed = remove_cups(current)
    removed_vals = [c.val for c in removed]
    print(f"pick up: " + ",".join(map(str, removed_vals))) if DEBUG_PRINT else ""

    destination_val = highest_val if current.val == 1 else current.val - 1
    while destination_val in removed_vals:
        destination_val = highest_val if destination_val == 1 else destination_val - 1
    destination = cup_by_val[destination_val]
    print(f"destination: {destination.val}") if DEBUG_PRINT else ""

    insert_cups(removed, destination)

def create_cups(initial, up_to):
    first = prev = None
    cup_by_val = {}

    # Create the initial cups
    initial_max = 0
    for v in initial:
        ival = int(v)
        c = Cup(ival, prev)
        cup_by_val[c.val] = c
        if not first:
            first = c
        prev = c
        if ival > initial_max:
            initial_max = ival

    # Extend the cups as needed
    for i in range(initial_max, up_to):
        c = Cup(i+1, prev)
        cup_by_val[c.val] = c
        prev = c

    prev.next = first
    first.prev = prev
    return (first,cup_by_val)

def main(args):
    global DEBUG_PRINT
    DEBUG_PRINT = args.debug
    max_cup = args.number_of_cups

    print(f"Number of cups: {max_cup}, Number of turns: {args.number_of_moves}")

    first,cup_by_val = create_cups(file_contents(args.file)[0], max_cup)

    current = first
    for i in range(args.number_of_moves):
        print(f"-- move {i+1} --") if DEBUG_PRINT else ""
        take_turn(current, max_cup, cup_by_val)
        current = current.next
    print_cups(current) if DEBUG_PRINT else ""

    one = cup_by_val[1]

    if DEBUG_PRINT:
        c = one.next
        s = []
        for i in range(max_cup - 1):
            s.append(c.sval)
            c = c.next
        print("".join(s))
            
    a = one.next.val
    b = one.next.next.val
    print(f"{a} * {b} = {a*b}")

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help='Input file, default: {}'.format(DEFAULT_INPUT_FILE), default=DEFAULT_INPUT_FILE, required=True)
    parser.add_argument('-v', '--verbose', help="Verbose output", default=False, action="store_true")
    parser.add_argument('-n', '--number_of_moves', help=f"Number of moves, default: {DEFAULT_MOVE_NUM}", type=int, default=DEFAULT_MOVE_NUM)
    parser.add_argument('-c', '--number_of_cups', help=f"Number of cups to use, default: {DEFAULT_CUP_NUM}", type=int, default=DEFAULT_CUP_NUM)
    parser.add_argument('--debug', help="Debug output", default=False, action="store_true")
    args = parser.parse_args()

    main(args)