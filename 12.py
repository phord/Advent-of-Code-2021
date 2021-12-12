#!/bin/python3

from core.skel import *

sample = """
start-A
start-b
A-c
A-b
b-d
A-end
b-end
"""

sample2="""
dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc"""

answer1 = None
answer2 = None

def parse(input):
    lines = [parse_fields(x,digits+alpha) for x in input.splitlines() if x]
    edges = {}
    for x in lines:
        a,b = x
        if a not in edges:
            edges[a] = set()
        if b not in edges:
            edges[b] = set()
        edges[a].add(b)
        edges[b].add(a)
    return edges

def traverse(edges, cave, path, visited, once):
    if cave != 'start' and cave in visited:
        once = True
    if cave >= 'a':
        visited = visited | set([cave])
    path = path[:]
    path.append(cave)

    if cave == 'end':
        yield ','.join(path)
    else:
        for dest in edges[cave] - (visited if once else set(['start'])):
            yield from traverse(edges, dest, path, visited, once)

def part1(edges, part2=False):
    return len(list(traverse(edges, 'start', [], set(), not part2)))

def part2(edges):
    return part1(edges, True)


from aocd import data
runAll(sample, data, parse, part1, part2, answer1, answer2)