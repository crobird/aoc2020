#!/usr/bin/env python

"""
Advent of Code 2020
"""

import os
import re
import math
import collections
import itertools
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
    def __init__(self, nums, fielddefs):
        self.nums = nums
        self.fielddefs = fielddefs
        self.fields = { f.name: None for f in fielddefs }
        self.complete = {}

    def __repr__(self):
        if self.complete:
            return f"Ticket({self.complete})"
        return f"Ticket({self.nums=})"

    def assign_field_values(self, field_indexes):
        for i,f in enumerate(self.fielddefs):
            if f.name not in field_indexes:
                self.complete[f.name] = self.nums[i]
            else:
                self.complete[f.name] = self.nums[field_indexes[f.name]]

    def get_definite_fields(self):
        num_matches = self.get_matching_nums_by_index()
        return {v[0]:k for k,v in num_matches.items() if len(v) == 1}

    def get_departure_values(self):
        return [v for f,v in self.complete.items() if f.startswith('departure')]

    def get_matching_nums_by_index(self):
        num_matches = {}
        for i,n in enumerate(self.nums):
            num_matches[i] = [f.name for f in self.fielddefs if f.matches(n)]
        return num_matches

    def get_nonmatching_nums_by_index(self):
        non_matches = {}
        for i,n in enumerate(self.nums):
            non_matches[i] = [f.name for f in self.fielddefs if not f.matches(n)]
        return non_matches


    def get_bad_fields(self):
        bad_fields = []
        for n in self.nums:
            matches = False
            for f in self.fielddefs:
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

def get_product(nums):
    if not nums:
        return 0
    rval = 1
    for n in nums:
        rval *= n
    return rval

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

    # Get valid tickets
    valid_tickets = []
    for t in nearby_tickets:
        bad_fields = t.get_bad_fields()
        if not bad_fields:
            valid_tickets.append(t)

    # Create mapping of field -> possible indices
    field_possibles = { f.name: list(range(len(fields))) for f in fields }
    for t in itertools.chain(valid_tickets, [t]):
        index_misses = t.get_nonmatching_nums_by_index()
        for i,fs in index_misses.items():
            for f in fs:
                if i in field_possibles[f]:
                    field_possibles[f].remove(i)

    # Reduce possible indices based on things with only one possibility
    definite_fields = {k:x[0] for k,x in field_possibles.items() if len(x) == 1}
    while len(definite_fields) < len(fields):
        for f,i in definite_fields.items():
            for k in field_possibles:
                if k != f and i in field_possibles[k]:
                    field_possibles[k].remove(i)
        definite_fields = {k:x[0] for k,x in field_possibles.items() if len(x) == 1}

    # Now that we know the values, we'll make the associations in our ticket object
    my_ticket.assign_field_values(definite_fields)

    print(my_ticket)

    # Calculate departure values
    product = get_product(my_ticket.get_departure_values())
    print(f"Departure product: {product}")



if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help='Input file, default: {}'.format(DEFAULT_INPUT_FILE), default=DEFAULT_INPUT_FILE, required=True)
    parser.add_argument('-v', '--verbose', help="Verbose output", default=False, action="store_true")
    args = parser.parse_args()

    main(args)