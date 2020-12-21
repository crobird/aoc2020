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
class Recipe:
    ingredients: [str]
    allergens: [str]


def file_contents(filepath, strip_empty_lines=True):
    empty_lines = not strip_empty_lines
    with open(filepath, "r") as fh:
        lines = [l.strip() for l in fh if (empty_lines or l.strip())]
    return lines


def parse_file(filepath):
    lines = file_contents(filepath)
    recipes = []
    for line in lines:

        # Parse with regex
        mobj = re.match(r'([\w\s]+) \(contains ([\w,\s]+)\)$', line)
        if mobj:
            ingredients = mobj.group(1).split(' ')
            allergens = mobj.group(2).split(', ')
            recipes.append(Recipe(ingredients, allergens))
    return recipes

def reduce_amap(known, amap):
    for a in amap:
        # If the ingredient is listed for a known allergen and the allergen doesn't map, remove it
        for i, v in known.items():
            if i in amap[a] and a != v:
                amap[a].remove(i)

def main(args):
    recipes = parse_file(args.file)

    # Build a lookup by allergen with the intersection of ingredients
    amap = {}
    for r in recipes:
        for a in r.allergens:
            if a not in amap:
                amap[a] = set(r.ingredients)
                continue
            amap[a] = amap[a].intersection(set(r.ingredients))

    # Try to work down the sets based on things we know, stop when we don't make new progress
    known = {list(s)[0]:a for a,s in amap.items() if len(s) == 1}
    last_count = None
    while len(known) != last_count:
        last_count = len(known)
        reduce_amap(known, amap)
        known = {list(s)[0]:a for a,s in amap.items() if len(s) == 1}

    count = 0
    for r in recipes:
        for i in r.ingredients:
            if i not in known:
                count += 1

    print(f"{count=}")

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help='Input file, default: {}'.format(DEFAULT_INPUT_FILE), default=DEFAULT_INPUT_FILE, required=True)
    parser.add_argument('-v', '--verbose', help="Verbose output", default=False, action="store_true")
    args = parser.parse_args()

    main(args)