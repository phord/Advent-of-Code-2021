#!/bin/python3

from core.skel import *

sample = """
3,4,3,1,2
"""
answer1 = 5934
answer2 = 26984457539

def parse(input):
    lines = [parse_fields(x,digits+alpha) for x in input.splitlines() if x][0]
    fish = [0]*9
    for x in lines:
        fish[x] += 1
    return fish

def part1(input, part2=False):
    out = input
    d = 18
    for d in range(256 if part2 else 80):
        newfish = out[0]
        out = out[1:]
        out[6] += newfish
        out.append(newfish)

    return sum(out)


def part2(input):
    return part1(input, True)

from aocd import data
actual = data

runAll(sample, actual, parse, part1, part2, answer1, answer2)