#!/bin/python3

from core.skel import *
from colorama import Fore, Style

CYAN = Fore.CYAN
GREEN = Fore.GREEN
YELLOW = Fore.YELLOW
RED = Fore.RED

sample = """
2199943210
3987894921
9856789892
8767896789
9899965678
"""
answer1 = 15
answer2 = 1134

floor = None
width, height = (None, None)

def lowest(x, y):
    measure = floor[y][x]
    if x > 0 and floor[y][x-1] <= measure:
        return False
    if x < width-1 and floor[y][x+1] <= measure:
        return False
    if y > 0 and floor[y-1][x] <= measure:
        return False
    if y < height-1 and floor[y+1][x] <= measure:
        return False
    return True

def fill(x, y, basin=set()):
    if x < 0 or y < 0 or x == width or y == height:
        return basin
    if floor[y][x] == 9:
        return basin
    if (x,y) in basin:
        return basin

    basin.add((x,y))
    basin = fill(x-1, y, basin)
    basin = fill(x+1, y, basin)
    basin = fill(x, y-1, basin)
    basin = fill(x, y+1, basin)
    return basin

def parse(input):
    global floor, width, height
    floor = [[int(a) for a in x] for x in input.splitlines() if x]
    width = len(floor[0])
    height = len(floor)
    return floor

def dump(basin):
    for y in range(height):
        line = ''
        for x in range(width):
            if (x,y) in basin:
                line += f"{GREEN}"
            else:
                line += f"{RED}"
            line += str(floor[y][x])
        print(line)
    print("----------------")



def part1(input, part2=False):
    total = 0
    for y in range(height):
        line = ''
        for x in range(width):
            if lowest(x,y):
                line += f"{GREEN}"
                # print (floor[y][x])
                total += 1 + floor[y][x]
            line += str(floor[y][x]) + f"{RED}"
        # print(line)
    return total


def part2(input):
    sizes = []
    for y in range(height):
        for x in range(width):
            if lowest(x,y):
                bx = fill(x, y, set())
                # dump(bx)
                sizes.append(len(bx))
                print (len(bx))
    sizes.sort()
    return sizes[-1] * sizes[-2] * sizes[-3]


from aocd import data
runAll(sample, data, parse, part1, part2, answer1, answer2)