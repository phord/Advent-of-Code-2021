#!/bin/python3

from core.skel import *

sample = """
..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###"""
answer1 = None
answer2 = None


# class Grid:

def parse(input):
    lines = [x for x in input.splitlines() if x]
    return lines

def to_grid(image):
    grid = set()
    for row in range(len(image)):
        for col in range(len(image[row])):
            if image[row][col] == '#':
                grid.add((row, col))
    return grid

def bit(image, row, col):
    default, size, grid = image
    tl, br = size
    x0,y0 = tl
    x1,y1 = br

    return (row,col) in grid or (default and (col < x0 or col > x1 or row < y0 or row > y1))

def binary(image, row, col):
    default, size, grid = image
    tl, br = size
    x0,y0 = tl
    x1,y1 = br

    str = []
    for r in range(row,row+3):
        str.extend([(r, c) for c in range(col, col+3)])
    b = 0
    for cell in str:
        b *= 2
        if bit(image, *cell):
            b += 1
    return b

def output(image, decoder, row, col):
    return decoder[binary(image, row, col)] == '#'

def step(image, decoder):
    default, size, _ = image
    tl, br = size
    x0,y0 = tl
    x1,y1 = br

    grid = set()
    for row in range(y0-2, y1+30):
        for col in range(x0-2, x1+3):
            if output(image, decoder, row, col):
                grid.add((row, col))

    default, _, _ = image
    if default:
        default = decoder[511] == '#'
    else:
        default = decoder[0] == '#'
    return (default, measure(grid), grid)

def measure(grid):
    x0,y0, x1,y1 = (0,0,0,0)
    # print(len(grid))
    for c in grid:
        y,x = c
        x0 = min(x, x0)
        y0 = min(y, y0)
        x1 = max(x, x1)
        y1 = max(y, y1)
    return ((x0,y0), (x1,y1))

def dump(image):
    default, size, grid = image
    tl, br = size
    x0,y0 = tl
    x1,y1 = br

    for row in range(y0-3, y1+1+3):
        str = ['#' if bit(image, row, col) else '.' for col in range(x0-3, x1+1+3)]
        print(''.join(str))
    print("---")


def part1(input, part2=False):
    decoder = input[0]
    image = input[1:]

    grid = to_grid(image)

    grid = (False, measure(grid), grid)

    for x in range(50 if part2 else 2):
        # dump(grid)
        grid = step(grid, decoder)
    dump(grid)


    return len(grid[2])


def part2(input):
    return part1(input, True)


from aocd import data
runAll(sample, data, parse, part1, part2, answer1, answer2)