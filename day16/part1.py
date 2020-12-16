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


class TicketField:
    def __init__(self, name, range_strs):
        self.name = name
        self.range_strs = range_strs
        self.ranges = []
        self.parse_ranges(range_strs)

    def parse_ranges(self, range_strs):
        for rs in range_strs:
            self.ranges.append(list(map(int, rs.split('-'))))

    def matches(self, v):
        for r in self.ranges:
            if v >= r[0] and v <= r[1]:
                return True
        return False

class Ticket:
    def __init__(self, nums, fields):
        self.nums = nums
        self.fields = fields

    def get_bad_fields(self):
        bad_fields = []
        for n in self.nums:
            matches = False
            for f in self.fields:
                if f.matches(n):
                    matches = True
                    break
            if not matches:
                bad_fields.append(n)
        return bad_fields

def file_contents(filepath, strip_empty_lines=True):
    empty_lines = not strip_empty_lines
    with open(filepath, "r") as fh:
        lines = [l.strip() for l in fh if (empty_lines or l.strip())]
    return lines


def parse_file(filepath):
    lines = file_contents(filepath)
    my_ticket = None
    nearby_tickets = []
    fields = []
    ticket_mode = 0
    for line in lines:
        # Parse with regex
        mobj = re.match(r'([\w\s]+): (\d+\-\d+) or (\d+\-\d+)', line)
        if mobj:
            fields.append(TicketField(mobj.group(1), [mobj.group(2), mobj.group(3)]))
            continue

        if line == 'your ticket:':
            ticket_mode = 1
            continue
        elif line == 'nearby tickets:':
            ticket_mode = 2
            continue

        if ticket_mode > 0:
            nums = list(map(int, line.split(',')))
            if ticket_mode == 1:
                my_ticket = Ticket(nums, fields)
            else:
                nearby_tickets.append(Ticket(nums, fields))
        else:
            print("Unexpected line: " + line)
            exit(1)

    return (fields, my_ticket, nearby_tickets)


def main(args):
    fields, my_ticket, nearby_tickets = parse_file(args.file)

    bad_sum = 0
    for t in nearby_tickets:
        bad_fields = t.get_bad_fields()
        bad_sum += sum(bad_fields)
    print(f"Scanning error rate: {bad_sum}")

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help='Input file, default: {}'.format(DEFAULT_INPUT_FILE), default=DEFAULT_INPUT_FILE, required=True)
    parser.add_argument('-v', '--verbose', help="Verbose output", default=False, action="store_true")
    args = parser.parse_args()

    main(args)