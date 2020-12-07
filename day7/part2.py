#!/usr/bin/env python

"""
Advent of Code 2020
bad answers:
5523 (too low)
"""

import os
import re
import math
import collections
from enum import Enum
from dataclasses import dataclass

me = os.path.basename(__file__)

DEFAULT_INPUT_FILE = "input/" + me.replace(".py", ".txt")

class Bag:
    def __init__(self, color):
        self.color = color
        self.content_requirements = dict()
        self.parents = set()

    def __repr__(self):
        return f"""
-- {self.color} --
{self.content_requirements=}
{self.parents=}
"""

    def add_content_requirements(self, content_requirements):
        self.content_requirements = content_requirements

    def add_parent_color(self, parent_color):
        self.parents.add(parent_color)

class Bags:
    def __init__(self):
        self.bags = dict()

    def add_bag(self, color, contents=None, parent_color=None):
        if color not in self.bags:
            self.bags[color] = Bag(color)
        if contents:
            self.bags[color].add_content_requirements(contents)
            for k in contents:
                self.add_bag(k, parent_color=color)
        elif parent_color:
            self.bags[color].add_parent_color(parent_color)

    def get_color_upstream_parents(self, color):
        parent_colors = set()
        if color not in self.bags:
            print(f"No entry for {color}, that's probably bad, bailing")
            exit(1)
        parent_list = self.bags[color].parents.copy()
        print(f"initial parent list for {color}: {parent_list}")
        while parent_list:
            p = parent_list.pop()
            print(f"Considering parent '{p}' that can be held in these bags: {self.bags[p].parents}")
            if p not in parent_colors:
                parent_colors.add(p)
                parent_list.update(self.bags[p].parents.copy())
        return parent_colors

    def get_required_children_count(self, color, indentlevel=0):
        count = 0
        indent = "\t"*indentlevel
        for k,v in self.bags[color].content_requirements.items():
            print(f"{indent}{color} contains {v} {k} bags")
            count += v + v * self.get_required_children_count(k, indentlevel+1)
        print(f"{indent}{color} needs {count} bags")
        return count


def parse_bag_requirements(filepath):
    bags = Bags()
    with open(filepath, "r") as fh:
        for l in fh:
            line = l.strip()
            if not line:
                continue
            m = re.match(r'([\w\s]+?) bags contain (.*)$', line)
            if not m:
                print(f"Error parsing line: {line}")
                exit(1)
            bag_color = m.group(1)
            contents = {}
            content_reqs = m.group(2).split(',')
            for req in content_reqs:
                if req.find("no other bags") != -1:
                    break
                m = re.match(r'(\d+) ([\w\s]+?) bags?\.?$', req.strip())
                if not m:
                    print(f"Error parsing req line: {req}")
                    exit(1)
                contents[m.group(2)] = int(m.group(1))
            bags.add_bag(bag_color, contents)
    return bags


def main(args):
    bags = parse_bag_requirements(args.file)

    # print(bags.bags['shiny gold'])
    required_subbags = bags.get_required_children_count('shiny gold')
    print(f"Required number of bags: {required_subbags}")



if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help='Input file, default: {}'.format(DEFAULT_INPUT_FILE), default=DEFAULT_INPUT_FILE, required=True)
    parser.add_argument('-v', '--verbose', help="Verbose output", default=False, action="store_true")
    args = parser.parse_args()

    main(args)