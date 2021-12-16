#!/bin/python3

from core.skel import *
from collections import defaultdict

import networkx as nx

sample = """
1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581
"""
answer1 = 40
answer2 = 315

def parse(input):
    grid = [[int (a) for a in x] for x in input.splitlines() if x]
    return grid

def times5(grid):
    ngrid = []
    for row in grid:
        ngrid.append(row[:])
        for i in range(4):
            ngrid[-1].extend([((x+i) % 9)+1 for x in row])

    for i in range(4):
        for row in ngrid[:len(grid)]:
            ngrid.append([((x+i) % 9)+1 for x in row])

    return ngrid

def dump(grid):
    for row in grid:
        print(row)
    print()

def to_grid(grid, cost):
    height = len(grid)
    width = len(grid[0])
    ret = []
    for y in range(height):
        row = [cost[(y,x)] for x in range(width)]
        ret.append(row)
    return ret

def dump(grid):
    height = len(grid)
    width = len(grid[0])
    for row in grid:
        print(row)
    print()

def neighbors(grid, pos, memo):
    if pos in memo:
        return memo[pos]

    height = len(grid)
    width = len(grid[0])
    y,x = pos
    ret = frozenset()
    for X in range(max([0,x-1]), min([width, x+2])):
        if X!=x:
            ret = ret | frozenset([(y,X)])
    for Y in range(max([0,y-1]), min([height, y+2])):
        if Y!=y :
            ret = ret | frozenset([(Y,x)])

    memo[pos] = ret
    # print(f"{pos}: {set(ret)}")
    return ret

def part1(grid, part2=False):
    height = len(grid)
    width = len(grid[0])

    cost = {}
    memo = {}
    G = nx.MultiDiGraph()
    for y in range(height):
        for x in range(width):
            cost = grid[y][x]
            for n in neighbors(grid, (y,x), memo):
                G.add_edge(n, (y,x), weight=cost)

    return nx.shortest_path_length(G, (0,0), (height-1, width-1), weight='weight', method='bellman-ford')

def part2(grid):
    grid = times5(grid)
    # dump(grid)
    return part1(grid, True)


from aocd import data
runAll(sample, data, parse, part1, part2, answer1, answer2)