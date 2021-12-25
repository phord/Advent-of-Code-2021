#!/bin/python3

from core.skel import *

sample = """
v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>"""
answer1 = None
answer2 = None

def parse(input):
    lines = [x for x in input.splitlines() if x]

    south = set()
    east = set()
    for row,line in enumerate(lines):
        for col,c in enumerate(line):
            if c == 'v':
                south.add((row,col))
            elif c == '>':
                east.add((row,col))

    return (east, south, (len(lines), len(lines[0])))

def move(orig, dir, pop, size):
    x = (orig[0] + dir[0]) % size[0]
    y = (orig[1] + dir[1]) % size[1]
    pos = (x,y)
    if pos in pop:
        return orig
    else:
        return pos

def step(east, south, size):
    east_next = set()
    south_next = set()
    pop = east | south
    for pos in east:
        east_next.add(move(pos, (0,1), pop, size))

    pop = east_next | south
    for pos in south:
        south_next.add(move(pos, (1,0), pop, size))

    return (east_next, south_next)

def dump(east, south, size):
    height, width  = size
    for row in range(height):
        line = ['>' if (row,col) in east else 'v' if (row,col) in south else '.' for col in range(width)]
        print(''.join(line))
    print("---")

def part1(input, part2=False):
    x = 0
    east, south, size = input
    while True:
        x += 1
        # dump(east, south, size)
        # print(x)
        east_next, south_next = step(east, south, size)
        if not (east_next - east or south_next - south):
            break
        east = east_next
        south = south_next

    return x


def part2(input):
    return part1(input, True)


from aocd import data
runAll(sample, data, parse, part1, part2, answer1, answer2)