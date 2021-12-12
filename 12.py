#!/bin/python3

from core.skel import *
from collections import defaultdict

sample = """
start-A
start-b
A-c
A-b
b-d
A-end
b-end
"""

answer1 = None
answer2 = None

def parse(input):
    edges = defaultdict(set)
    for x in filter(lambda _:_, input.splitlines()):
        A,B = x.split('-')
        for a,b in [(A,B), (B,A)]:
            if a != 'end' and b != 'start':
                edges[a].add(b)
    return edges

def traverse(edges, cave, path, visited, once):
    once |= cave in visited
    if cave >= 'a':
        visited = visited | set([cave])

    path.append(cave)
    if cave == 'end':
        yield ','.join(path)
    else:
        for dest in edges[cave] - visited if once else edges[cave]:
            yield from traverse(edges, dest, path, visited, once)
    path.pop()

def part1(edges, part2=False):
    return len(list(traverse(edges, 'start', [], set(), not part2)))

def part2(edges):
    return part1(edges, True)

from aocd import data
runAll(sample, data, parse, part1, part2, answer1, answer2)