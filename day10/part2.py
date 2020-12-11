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

@dataclass
class Adapter:
    index: int
    jolts: int
    possibles: [int]

def file_contents(filepath, strip_empty_lines=True):
    empty_lines = not strip_empty_lines
    with open(filepath, "r") as fh:
        lines = [l.strip() for l in fh if (empty_lines or l.strip())]
    return lines

def get_next_adapters(from_jolts, jolt_list, start_index):
    i = start_index
    matches = []
    while True:
        diff = jolt_list[i] - from_jolts
        if diff > 3:
            break
        matches.append(jolt_list[i])
        i += 1
        if i == len(jolt_list):
            break
    print(f"{from_jolts} -> {matches}")
    return matches

def traverse_nodes(nodes, curr=0):
    possible_routes = 0
    for p in nodes[curr].possibles:
        possible_routes += traverse_nodes(nodes, p.index)
    if len(nodes[curr].possibles) > 1:
        return possible_routes + len(nodes[curr].possibles) - 1
    return possible_routes


def traverse_nodes2(nodes, index_offset=0, curr=0):
    if curr >= len(nodes):
        return 1
    possible_routes = 0
    possible_vals = [x.jolts for x in nodes[curr].possibles]
    print(f"node.jolts={nodes[curr].jolts}, node.index={nodes[curr].jolts}, {curr=}, {index_offset=}, possibles={possible_vals}")
    for p in nodes[curr].possibles:
        index = p.index - index_offset
        print(f"following {p.jolts}: {index=}, {index_offset=}")
        possible_routes += traverse_nodes2(nodes, index_offset, index)
    return possible_routes

def multem(l):
    if not l:
        return
    total = 1
    for i in l:
        total *= i
    return total

def nodeprint(nodes):
    for n in nodes:
        plist = [(x.index,x.jolts) for x in n.possibles]
        print(f"{n.index=} -> {plist}")

def main(args):
    ratings = list(map(int, file_contents(args.file)))
    ratings.sort()
    ratings.insert(0,0)

    # Convert list into Adapter nodes
    nodes = [None]*len(ratings)
    curr = 0
    for i,r in enumerate(ratings):
        if not nodes[i]:
            nodes[i] = Adapter(i, r, [])
        matches = get_next_adapters(r, ratings, i+1) if i < len(ratings) - 1 else []
        for j,mr in enumerate(matches):
            m_index = i + 1 + j
            mn = Adapter(m_index, mr, []) if not nodes[m_index] else nodes[m_index]
            nodes[i].possibles.append(mn)

    if False:
        print("Traversing nodes...")
        total = traverse_nodes(nodes)
        print(total+1)


    # Traverse nodes, isolating chunks between single paths and identifying the count
    # of possibilities within. Then multiplying those numbers at the end.
    s = 0
    chunk = []
    chunk_offset = None
    chunk_results = []
    for i,n in enumerate(nodes):
        p = len(n.possibles)
        if p > 1:
            if chunk_offset is None:
                chunk_offset = i
            chunk.append(n)
        else:
            if chunk:
                if chunk_offset is None:
                    print("Whaaaa")
                    exit(1)
                chunk.append(n)
                nodeprint(chunk)
                total = traverse_nodes2(chunk, chunk_offset)
                print(f"{total=}, {chunk=}, {chunk_offset=}")
                chunk_results.append(total) # This should be traversal
                chunk = []
                chunk_offset = None
    
    print(f"{chunk_results=}, multed={multem(chunk_results)}")


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help='Input file, default: {}'.format(DEFAULT_INPUT_FILE), default=DEFAULT_INPUT_FILE, required=True)
    parser.add_argument('-v', '--verbose', help="Verbose output", default=False, action="store_true")
    args = parser.parse_args()

    main(args)