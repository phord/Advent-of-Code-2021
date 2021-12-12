#!/bin/python3

from core.skel import *

sample = """
5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526
"""
answer1 = 1656
answer2 = 195

flashes = 0

def parse(input):
    lines = [[int(y) for y in x] for x in input.splitlines() if x]
    return lines

def flash(grid, x, y):
    for X in range(max([0, x-1]),min([x+2, 10])):
        for Y in range(max([0, y-1]),min([y+2, 10])):
            inc(grid, X, Y)

def inc(grid, x, y):
    grid[x][y] += 1
    if grid[x][y] == 10:
        flash(grid, x, y)

def rollover(grid):
    global flashes
    for y in range(10):
        for x in range(10):
            if grid[x][y] > 9:
                grid[x][y] = 0
                flashes += 1

def step(grid):
    for y in range(10):
        for x in range(10):
            inc(grid, x, y)
    rollover(grid)

def part1(input, part2=False):
    global flashes
    flashes = 0

    prev = flashes
    for x in range(10000 if part2 else 100):
        step(input)
        if part2 and flashes - prev == 100:
            return x+1
        prev = flashes
        # print(x, flashes)
    return flashes


def part2(input):
    return part1(input, True)


from aocd import data
runAll(sample, data, parse, part1, part2, answer1, answer2)