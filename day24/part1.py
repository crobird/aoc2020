#!/usr/bin/env python

"""
Advent of Code 2020

Using 2D array for my hex board by shifting rows. Here's an example of how you
can see how it's done:

    board = Board(5)
    x = board.center
    board.flip_xy(*x)
    board.flip_dir_xy(*x, 'w')
    board.flip_dir_xy(*x, 'e')
    board.flip_dir_xy(*x, 'sw')
    board.flip_dir_xy(*x, 'se')
    board.flip_dir_xy(*x, 'nw')
    board.flip_dir_xy(*x, 'ne')

    board.print()
    print("\n\n")
    board.print_unshifted()

"""

import os
import re
import math
import collections
from enum import Enum
from datetime import datetime, timedelta
from dataclasses import dataclass

me = os.path.basename(__file__)

DEFAULT_INPUT_FILE = "input/" + me.replace(".py", ".txt")
STARTED_AT = None


class Color(Enum):
    BLACK = 0
    WHITE = 1
    def inv(self):
        return Color((self.value + 1) % 2)

class Board:
    """
    We are going to make a hex board using a 2D array.
    Even rows will skew left, such that:
    - an even row cell at N will have NW and NE neighbors at N and N+1
    - an odd row cell at N will have NW and NE neighbors at N-1 and N.
    """
    dirmap = {
        ('e', 0): (1,0),
        ('e', 1): (1,0),
        ('se',0): (0,1),
        ('se',1): (1,1),
        ('sw',0): (-1,1),
        ('sw',1): (0,1),
        ('w', 0): (-1,0),
        ('w', 1): (-1,0),
        ('nw',0): (-1,-1),
        ('nw',1): (0,-1),
        ('ne',0): (0,-1),
        ('ne',1): (1,-1),
    }

    def __init__(self, distance):
        self.distance = distance
        self.board_size = (distance * 2) + 1
        self.board = [[Color.WHITE for i in range(self.board_size)] for j in range(self.board_size)]        

    def __repr__(self):
        return f"Board(size={self.board_size}, black_count={self.black_count})"

    @property
    def black_count(self):
        total = 0
        for row in self.board:
            total += row.count(Color.BLACK)
        return total

    @property
    def center(self):
        return (self.distance, self.distance)

    def print(self):
        gap = ' '
        for i,row in enumerate(self.board):
            leading_space = gap*(i % 2)
            s = leading_space + gap.join([str(x.value) for x in row])
            print(s)

    def print_unshifted(self):
        for row in self.board:
            print(" ".join([str(x.value) for x in row]))

    def dir_xy(self, x, y, direction):
        is_odd = y % 2
        offsets = Board.dirmap[(direction,y%2)]
        return (x+offsets[0], y+offsets[1])

    def dir_color(self, *args, **kwargs):
        xy = self.dir_xy(*args, **kwargs)
        return self.board[xy[1]][xy[0]]

    def flip_dir_xy(self, *args, **kwargs):
        xy = self.dir_xy(*args, **kwargs)
        self.board[xy[1]][xy[0]] = self.board[xy[1]][xy[0]].inv()

    def flip_xy(self, x, y):
        self.board[y][x] = self.board[y][x].inv()


class TileDirections:
    def __init__(self, instructions):
        self.instructions = []
        self.max_instruction_length = 0
        self.parse_instructions(instructions)

    def __repr__(self):
        return f"{self.instructions}\n{max_instruction_length=}"

    def parse_instructions(self, instructions):
        for i in instructions:
            s = i
            directions = []
            while len(s):
                if s[0] in ['n','s']:
                    directions.append(s[:2])
                    s = s[2:]
                else:
                    directions.append(s[0])
                    s = s[1:]
            self.instructions.append(directions)
        self.max_instruction_length = max([len(i) for i in self.instructions])

def log_start():
    global STARTED_AT
    STARTED_AT = datetime.now()
    print(f"[{STARTED_AT}]")

def log_end():
    global STARTED_AT
    duration = datetime.now() - STARTED_AT
    print(f"[execution time: {duration}]")

def file_contents(filepath, strip_empty_lines=True):
    empty_lines = not strip_empty_lines
    with open(filepath, "r") as fh:
        lines = [l.strip() for l in fh if (empty_lines or l.strip())]
    return lines

def main(args):
    log_start()
    # ---------

    things = file_contents(args.file)
    td = TileDirections(things)
    board = Board(td.max_instruction_length)

    for ins in td.instructions:
        xy = board.center
        for d in ins:
            xy = board.dir_xy(*xy, d)
        board.flip_xy(*xy)

    board.print()
    print(board)

    # ---------
    log_end()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help='Input file, default: {}'.format(DEFAULT_INPUT_FILE), default=DEFAULT_INPUT_FILE, required=True)
    parser.add_argument('-v', '--verbose', help="Verbose output", default=False, action="store_true")
    args = parser.parse_args()

    main(args)