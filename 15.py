#!/bin/python3

from core.skel import *
from collections import defaultdict

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

def optimize(grid, cost, pos, memo):
    height = len(grid)
    width = len(grid[0])
    y,x = pos
    t = grid[y][x]
    opts = []
    for n in neighbors(grid, pos, memo):
        opts.append(cost[n])

    # print(f"{pos}: {neighbors(grid, pos, memo)}")

    prev = cost[pos]
    new = t + min(opts)
    if prev > new:
        # print("Improved ", pos)
        cost[(y,x)] = new
        return neighbors(grid, pos, memo) | frozenset([pos])
    return frozenset()

def part1(grid, part2=False):
    height = len(grid)
    width = len(grid[0])

    cost = {}
    for y in range(height-1, -1, -1):
        for x in range(width-1, -1, -1):
            t = grid[y][x]
            opts = []
            if y < height-1:
                opts.append(cost[(y+1, x)])

            if x < width-1:
                opts.append(cost[(y, x+1)])

            if opts:
                cost[(y,x)] = t + min(opts)
            else:
                cost[(y,x)] = t

    memo = {}
    changed = cost.keys()
    while changed:
        # dump(to_grid(grid, cost))

        print(len(changed))
        affected = set()
        for pos in changed:
            affected |= set(optimize(grid, cost, pos, memo))
        changed = affected

    # dump(grid)
    # dump(to_grid(grid, cost))
    return cost[(0, 0)] - grid[0][0]


def part2(grid):
    grid = times5(grid)
    # dump(grid)
    return part1(grid, True)


from aocd import data
runAll(sample, data, parse, part1, part2, answer1, answer2)