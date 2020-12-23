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
DEFAULT_MOVE_NUM = 100
DEFAULT_CUP_TAKE = 3

def file_contents(filepath, strip_empty_lines=True):
    empty_lines = not strip_empty_lines
    with open(filepath, "r") as fh:
        lines = [l.strip() for l in fh if (empty_lines or l.strip())]
    return lines

def get_destination_index(cups, original_cup_size, current_val):
    new_v = lambda x: x - 1 if x != 1 else 9
    v = new_v(current_val)
    while True:
        if v not in cups:
            v = new_v(v)
        else:
            return (cups.index(v),v)

def take_turn(cups, current, cup_take=DEFAULT_CUP_TAKE):
    current_val = cups[current]
    cup_size = len(cups)
    selected = []
    take_index = current + 1

    # Take out the next cups
    for i in range(cup_take):
        index = take_index if take_index < len(cups) else 0
        selected.append(cups.pop(index))
    print(f"pick up: {selected}")

    # Find destination cup
    current = cups.index(current_val)
    destination_index,destination_value = get_destination_index(cups, cup_size, current_val)
    print(f"destination: {destination_value}")
    # print(f"get_destination_index(): {current_val=}, {cups=}, {destination_index=}, {destination_value=}")

    # Reassemble the cup ring
    return cups[:destination_index+1] + selected + cups[destination_index+1:]

def print_cups(cups, current):
    x = []
    for i,v in enumerate(cups):
        if i == current:
            x.append(f"({v})")
        else:
            x.append(str(v))
    print(f"cups: " + " ".join(x))


def main(args):
    cups = [int(c) for c in file_contents(args.file)[0]]
    current_index = 0
    for i in range(args.number_of_moves):
        print(f"-- move {i+1} --")
        current_val = cups[current_index]
        print_cups(cups, current_index)
        cups = take_turn(cups, current_index)
        current_index = (cups.index(current_val) + 1) % len(cups)
        print("")
    
    cup_index = cups.index(1) + 1
    output = []
    for i in range(len(cups) - 1):
        index = (cup_index+i) % len(cups)
        output.append(cups[index])

    print("".join(map(str,output)))

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help='Input file, default: {}'.format(DEFAULT_INPUT_FILE), default=DEFAULT_INPUT_FILE, required=True)
    parser.add_argument('-v', '--verbose', help="Verbose output", default=False, action="store_true")
    parser.add_argument('-n', '--number_of_moves', help=f"Number of moves, default: {DEFAULT_MOVE_NUM}", type=int, default=DEFAULT_MOVE_NUM)
    args = parser.parse_args()

    main(args)