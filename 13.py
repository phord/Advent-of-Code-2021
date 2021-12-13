#!/bin/python3

from core.skel import *

sample = """
6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5"""
answer1 = None
answer2 = None

def fold_up(grid, row):
    out = set()
    for coord in grid:
        x,y = coord
        if y > row:
            out.add((x,2*row - y))
        else:
            out.add(coord)
    return out

def fold_left(grid, row):
    out = set()
    for coord in grid:
        x,y = coord
        if x > row:
            out.add(((2*row - x), y))
        else:
            out.add(coord)
    return out


def dump(grid):
    for y in range(20):
        line = ''
        for x in range(120):
            line += '#' if (x,y) in grid else '.'
        print(line)

def parse(input):
    return input.splitlines()

def part1(input, part2=False):
    grid = set()
    for line in input:
        if line:
            if ',' in line:
                a,b = line.split(',')
                a = int(a)
                b = int(b)
                grid.add((a,b))
            else:
                which,x = line.split()[-1].split('=')
                x = int(x)
                if which == 'y':
                    grid = fold_up(grid, x)
                else:
                    grid = fold_left(grid, x)
                if not part2:
                    break

    dump(grid)
    return len(grid)


def part2(input):
    return part1(input, True)


from aocd import data
runAll(sample, data, parse, part1, part2, answer1, answer2)