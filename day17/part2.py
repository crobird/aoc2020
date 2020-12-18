#!/usr/bin/env python

"""
Advent of Code 2020

bad answers:
"""

import os
import re
import math
import collections
import itertools
from enum import Enum
from copy import deepcopy
from dataclasses import dataclass

me = os.path.basename(__file__)

DEFAULT_INPUT_FILE = "input/" + me.replace(".py", ".txt")

CUBE_ACTIVE = '#'
CUBE_INACTIVE = '.'

@dataclass
class Cube:
    state: str
    x: int
    y: int
    z: int = 0
    w: int = 0

    @staticmethod
    def get_dict_key(x, y, z, w):
        return f"{x}.{y}.{z}.{w}"

    @property
    def dict_key(self):
        return Cube.get_dict_key(self.x, self.y, self.z, self.w)

class Cubes:
    def __init__(self, cubes, xy_size, z_size=1, w_size=1, cycle=0):
        self.cubes = cubes
        self.xy_size = xy_size
        self.z_size = z_size
        self.w_size = w_size
        self.cycle = cycle

    def __repr__(self):
        lines = []
        if self.z_size == 1:
            lines.extend(self.cubestr_at_z(0))
        else:
            for z in self.get_z_range():
                lines.extend(self.cubestr_at_z(z))
        return "\n".join(lines)

    @staticmethod
    def edge_index_for_n_items(n):
        if n != 0:
            return math.floor(n/2)
        return 0

    @staticmethod
    def range_for_n_items(n):
        edge = Cubes.edge_index_for_n_items(n)
        extra = n % 2
        return range(-edge, edge + extra)

    def get_z_range(self):
        return Cubes.range_for_n_items(self.z_size)

    def get_w_range(self):
        return Cubes.range_for_n_items(self.w_size)

    def get_xy_range(self):
        return Cubes.range_for_n_items(self.xy_size)
    
    def cubestr_at_z(self, z):
        lines = []
        lines.append(f"z={z}")
        for i in self.get_xy_range():
            chars = []
            for j in self.get_xy_range():
                k = Cube.get_dict_key(j, i, z)
                if k not in self.cubes:
                    print(f"Error: {k} not found in self.cubes, cannot print")
                else:
                    chars.append(self.cubes[k].state)
            lines.append(''.join(chars))
        lines.append("\n")
        return lines

    def get_cube_neigbors(self, x, y, z, w):
        return [Cube.get_dict_key(x+p[0], y+p[1], z+p[2], w+p[3]) for p in itertools.product([-1,0,1], repeat=4) if p.count(0) != 4]

    def run_cycle(self, print_cubes=False):
        next_cubes = deepcopy(self.cubes)

        self.xy_size += 2
        self.z_size += 2
        self.w_size += 2
        self.cycle += 1


        print(f"-- Starting cycle {self.cycle}, {self.z_size=}, {self.w_size=}, {self.xy_size=} --\n")

        for w in self.get_w_range():
            for z in self.get_z_range():
                for y in self.get_xy_range():
                    for x in self.get_xy_range():
                        cube_key = Cube.get_dict_key(x,y,z,w)
                        cube_neighbors = self.get_cube_neigbors(x, y, z, w)
                        if cube_key in self.cubes:
                            cube_state = self.cubes[cube_key].state
                        else:
                            cube_state = CUBE_INACTIVE
                            next_cubes[cube_key] = Cube(cube_state, x, y, z, w)

                        # Count how many neighbors are active
                        active_neighbors = [self.cubes[nk].state for nk in cube_neighbors if nk in self.cubes].count(CUBE_ACTIVE)

                        # Set next_cubes
                        if cube_state == CUBE_ACTIVE:
                            cube_state = CUBE_ACTIVE if active_neighbors in [2,3] else CUBE_INACTIVE
                        else:
                            cube_state = CUBE_ACTIVE if active_neighbors == 3 else CUBE_INACTIVE

                        next_cubes[cube_key].state = cube_state

        self.cubes = next_cubes

        if print_cubes:
            print(f"After {self.cycle} cycle{'s' if self.cycle != 1 else ''}\n" + self.__repr__())

    def count_active(self):
        active = 0
        for w in self.get_w_range():
            for z in self.get_z_range():
                for y in self.get_xy_range():
                    for x in self.get_xy_range():
                        cube_key = Cube.get_dict_key(x,y,z,w)
                        if self.cubes[cube_key].state == CUBE_ACTIVE:
                            active += 1
        return active


def file_contents(filepath, strip_empty_lines=True):
    empty_lines = not strip_empty_lines
    with open(filepath, "r") as fh:
        lines = [l.strip() for l in fh if (empty_lines or l.strip())]
    return lines


def parse_file(filepath):
    lines = file_contents(filepath)
    cubes = {}

    for line_index,i in enumerate(Cubes.range_for_n_items(len(lines))):
        line = lines[line_index]
        for s,j in enumerate(Cubes.range_for_n_items(len(lines))):
            cube = Cube(line[s],j,i)
            cubes[cube.dict_key] = cube
    return (cubes,len(lines))



def main(args):
    cubes,xy_size = parse_file(args.file)
    cubes = Cubes(cubes, xy_size)
    # print(cubes)
    for n in range(args.cycles):
        p_bool = True if args.print or (args.print_last and n == args.cycles - 1) else False
        cubes.run_cycle(print_cubes=p_bool)
    active_count = cubes.count_active()
    print(f"Active cubes after {args.cycles} cycles: {active_count}")

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help='Input file, default: {}'.format(DEFAULT_INPUT_FILE), default=DEFAULT_INPUT_FILE, required=True)
    parser.add_argument('-v', '--verbose', help="Verbose output", default=False, action="store_true")
    parser.add_argument('-c', '--cycles', help="Cycles to run, default=6", type=int, default=6)
    parser.add_argument('-p', '--print', help="Print all cycles", default=False, action="store_true")
    parser.add_argument('-P', '--print_last', help="Print last cycle", default=False, action="store_true")
    args = parser.parse_args()

    main(args)