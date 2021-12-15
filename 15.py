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

    changed = True
    while changed:
        changed = False
        print(cost[(0,0)])
        for y in range(height):
            for x in range(width):
                t = grid[y][x]
                opts = []
                if y < height-1:
                    opts.append(cost[(y+1, x)])

                if x < width-1:
                    opts.append(cost[(y, x+1)])

                if y > 0:
                    opts.append(cost[(y-1, x)])

                if x > 0:
                    opts.append(cost[(y, x-1)])

                if opts:
                    prev = cost[(y,x)]
                    new = t + min(opts)
                    if prev > new:
                        cost[(y,x)] = new
                        changed = True

    # dump(grid)
    # dump(to_grid(grid, cost))
    return cost[(0, 0)] - grid[0][0]


def part2(grid):
    grid = times5(grid)
    # dump(grid)
    return part1(grid, True)


from aocd import data
runAll(sample, data, parse, part1, part2, answer1, answer2)