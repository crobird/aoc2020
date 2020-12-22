#!/usr/bin/env python

"""
Advent of Code 2020
"""

import os
import re
import math
import collections
from enum import Enum
from copy import copy,deepcopy
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

def make_checksum(cards):
    total = 0
    for i,n in enumerate(cards):
        total += (i * 10) * n
    return total

def weve_been_here_before(players, history):
    checksums = [make_checksum(p) for p in players]
    # print(f"checksums for {players}: {checksums}")
    if checksums in history:
        return True
    history.append(checksums)
    return False

def play_game(players, debug=False):
    history = []
    while all([len(p) for p in players]):
        if weve_been_here_before(players, history):
            return 0
        cards = [p.pop(0) for p in players]
        if all([len(p)>=cards[i] for i,p in enumerate(players)]):
            # Play recursive
            player_copy = deepcopy(players)
            player_copy = [player_copy[i][:n] for i,n in enumerate(cards)]
            winner_index = play_game(player_copy)

            players[winner_index].append(cards.pop(winner_index))
            players[winner_index].extend(cards)
        else:
            winner_index = play_hand(cards)
            cards.sort(reverse=True)
            players[winner_index].extend(cards)
        if debug:
            print(players)
    return [i for i in range(len(players)) if len(players[i])][0]

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
    play_game(players, debug=True)
    score = score_game(players)
    print(score)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help='Input file, default: {}'.format(DEFAULT_INPUT_FILE), default=DEFAULT_INPUT_FILE, required=True)
    parser.add_argument('-v', '--verbose', help="Verbose output", default=False, action="store_true")
    args = parser.parse_args()

    main(args)