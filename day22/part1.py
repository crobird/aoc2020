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


def file_contents(filepath, strip_empty_lines=True):
    empty_lines = not strip_empty_lines
    with open(filepath, "r") as fh:
        lines = [l.strip() for l in fh if (empty_lines or l.strip())]
    return lines


def parse_file(filepath):
    lines = file_contents(filepath)
    players = []
    player = None
    cards = []
    for line in lines:

        # Parse with regex
        mobj = re.match(r'Player (\d+):', line)
        if mobj:
            if player:
                players.append(cards)
            player = int(mobj.group(1))
            cards = []

        elif line.isdigit():
            cards.append(int(line))

        else:
            raise Exception("Got unexpected line: " + line)
    if player:
        players.append(cards)

    return players

def play_hand(cards):
    highest = max(cards)
    return cards.index(highest)

def play_game(players):
    while all([len(p) for p in players]):
        cards = [p.pop(0) for p in players]
        winner_index = play_hand(cards)
        cards.sort(reverse=True)
        players[winner_index].extend(cards)

def score_game(players):
    total = 0
    for p in players:
        if len(p):
            p.reverse()
            for i,n in enumerate(p):
                total += (i+1) * n
    return total

def main(args):
    players = parse_file(args.file)
    play_game(players)
    score = score_game(players)
    print(score)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help='Input file, default: {}'.format(DEFAULT_INPUT_FILE), default=DEFAULT_INPUT_FILE, required=True)
    parser.add_argument('-v', '--verbose', help="Verbose output", default=False, action="store_true")
    args = parser.parse_args()

    main(args)