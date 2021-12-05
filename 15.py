#!/bin/python3

from core.skel import *

sample = """
"""

def parse(input):
    lines = [parse_fields(x,digits+alpha) for x in input.splitlines() if x]
    return lines

def part1(input, part2=False):
    return None


def part2(input):
    return part1(input, True)

actual = """
"""

runAll(sample, actual, parse, part1, part2)