#!/bin/python3

from core.skel import *

sample = """
..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###"""
answer1 = 35
answer2 = 3351

def parse(input):
    lines = [x for x in input.splitlines() if x]
    return lines

class Image:

    def __init__(self, input):
        self.from_input(input)

    def from_input(self, lines):
        self.decoder = [x=='#' for x in lines[0]]
        self.grid = set()
        self.default_lit = False        # The world outside our mapped cells is dark

        for row in range(1,len(lines)):
            for col in range(len(lines[row])):
                if lines[row][col] == '#':
                    self.grid.add((row-1, col))
        self.x0, self.y0, self.x1, self.y1 = (0, 0, row-1, col)

    def read_pixel(self, row, col):
        if col < self.x0 or col > self.x1 or row < self.y0 or row > self.y1:
            return self.default_lit
        else:
            return (row,col) in self.grid

    def binary(self, row, col):
        map = [(r, c) for r in range(row,row+3) for c in range(col, col+3) ]
        b = 0
        for cell in map:
            b *= 2
            if self.read_pixel(*cell):
                b += 1
        return b

    def step(self):
        next = set()
        for row in range(self.y0-2, self.y1+2):
            for col in range(self.x0-2, self.x1+2):
                if self.decoder[self.binary(row, col)]:
                    next.add((row, col))

        self.grid = next
        self.default_lit = self.decoder[511 if self.default_lit else 0]
        self.measure()

    def measure(self):
        exes = [_[1] for _ in self.grid]
        whys = [_[0] for _ in self.grid]
        self.x0 = min(exes)
        self.y0 = min(whys)
        self.x1 = max(exes)
        self.y1 = max(whys)

    def dump(self):
        print(f"{self.x0}, {self.y0} -- {self.x1}, {self.y1}")
        margin = 3
        for row in range(self.y0-margin, self.y1+1+margin):
            str = ['#' if self.read_pixel(row, col) else '.' for col in range(self.x0-margin, self.x1+1+margin)]
            print(f"{row}.", ''.join(str))
        print("---")


def part1(input, part2=False):
    grid = Image(input)

    for x in range(50 if part2 else 2):
        grid.step()
    # grid.dump()

    return len(grid.grid)


def part2(input):
    return part1(input, True)

from aocd import data
runAll(sample, data, parse, part1, part2, answer1, answer2)