#!/usr/bin/env python

"""
Advent of Code 2020

bad answers:
26
"""

import os
import re
import math
import collections
from enum import Enum
from dataclasses import dataclass

me = os.path.basename(__file__)

DEFAULT_INPUT_FILE = "input/" + me.replace(".py", ".txt")

class Group(object):
    def __init__(self, group_lines):
        self.qs = {}
        self.lines = group_lines
        self.people_count = len(group_lines)
        for l in group_lines:
            print(f"{l=}, {self.qs=}")
            for c in l:
                if c not in self.qs:
                    self.qs[c] = 0
                self.qs[c] += 1

    @property
    def yes_question_total(self):
        return len(self.qs.keys())
    

def parse_answers(filepath):
    groups = []
    with open(filepath, "r") as fh:
        group = []
        for l in fh:
            if not l.strip():
                if group:
                    groups.append(Group(group))
                    group = []
                continue
            group.append(l.strip())

        if group:
            groups.append(Group(group))

    return groups


def main(args):
    things = parse_answers(args.file)

    total = 0
    for t in things:
        total += t.yes_question_total

    print(f"Total count: {total}")

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help='Input file, default: {}'.format(DEFAULT_INPUT_FILE), default=DEFAULT_INPUT_FILE, required=True)
    parser.add_argument('-v', '--verbose', help="Verbose output", default=False, action="store_true")
    args = parser.parse_args()

    main(args)