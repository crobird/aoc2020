#!/usr/bin/env python

"""
Advent of Code 2020

bad answers:
115
"""

import os
import re
import math
import collections
from enum import Enum
from dataclasses import dataclass

me = os.path.basename(__file__)

DEFAULT_INPUT_FILE = "input/" + me.replace(".py", ".txt")

class Passport(object):
    def __init__(self, colon_separated_keyvals):
        self.initial_values = colon_separated_keyvals
        self.total_fields = len(colon_separated_keyvals)
        for kv in colon_separated_keyvals:
            k,v = kv.split(':')
            setattr(self, k, v)

    def __repr__(self):
        return f"{self.initial_values}"

    def has_required_fields(self):
        return self.total_fields - int(hasattr(self, 'cid')) == 7

    def int_between(self, v, lower, upper):
        return int(v) >= lower and int(v) <= upper

    def is_valid_byr(self):
        v = getattr(self, 'byr', None)
        if not v:
            return False
        return bool(re.match(r'\d{4}$', v)) and self.int_between(v, 1920, 2002) 

    def is_valid_iyr(self):
        v = getattr(self, 'iyr', None)
        if not v:
            return False
        return bool(re.match(r'\d{4}$', v)) and self.int_between(v, 2010, 2020) 

    def is_valid_eyr(self):
        v = getattr(self, 'eyr', None)
        if not v:
            return False
        return bool(re.match(r'\d{4}$', v)) and self.int_between(v, 2020, 2030) 

    def is_valid_hgt(self):
        v = getattr(self, 'hgt', None)
        if not v:
            return False
        m = re.match(r'(\d+)(cm|in)$', v)
        if not m:
            return False
        cm_or_in = m.group(2)
        h = int(m.group(1))
        return (cm_or_in == 'cm' and self.int_between(h, 150, 193)) or (cm_or_in == 'in' and self.int_between(h, 59, 76))

    def is_valid_hcl(self):
        v = getattr(self, 'hcl', None)
        if not v:
            return False
        return bool(re.match(r'#[0-9a-f]{6}$', v))

    def is_valid_ecl(self):
        v = getattr(self, 'ecl', None)
        if v in "amb blu brn gry grn hzl oth".split(' '):
            return True
        return False

    def is_valid_pid(self):
        v = getattr(self, 'pid', None)
        if not v:
            return False
        return bool(re.match(r'\d{9}$', v))

    def is_valid(self):
        return self.has_required_fields() and \
        self.is_valid_byr() and \
        self.is_valid_iyr() and \
        self.is_valid_eyr() and \
        self.is_valid_hgt() and \
        self.is_valid_hcl() and \
        self.is_valid_ecl() and \
        self.is_valid_pid()


def parse_passports(filepath):
    passports = []
    with open(filepath, "r") as fh:
        pbits = []
        for l in fh:
            line = l.strip()
            if line:
                pbits.extend(line.split(' '))
            elif pbits:
                passports.append(Passport(pbits))
                pbits = []
        if pbits:
            passports.append(Passport(pbits))
    return passports


def main(args):
    passports = parse_passports(args.file)

    if args.debug_field:
        print([getattr(p, args.debug_field, None) for p in passports if p.is_valid()])
        exit(1)

    valid = [p.is_valid() for p in passports].count(True)
    print(f"Out of {len(passports)} passports, there are {valid} valid ones.")


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help='Input file, default: {}'.format(DEFAULT_INPUT_FILE), default=DEFAULT_INPUT_FILE, required=True)
    parser.add_argument('-v', '--verbose', help="Verbose output", default=False, action="store_true")
    parser.add_argument('-F', '--debug_field', help="Field to debug")
    args = parser.parse_args()

    main(args)