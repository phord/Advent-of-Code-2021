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

count = 0
def traverse(edges, cave, path, visited, once):
    global count
    if cave != 'start' and cave in visited:
        once = True
    if cave >= 'a':
        visited = visited | set([cave])
    path = [x for x in path]
    path.append(cave)
    if cave == 'end':
        count += 1
        # print(f"{count}. {once} {','.join(path)}")
        return

    for dest in edges[cave] - (visited if once else set(['start'])):
        traverse(edges, dest, path, visited, once)

def part1(edges, part2=False):
    global count
    count = 0
    traverse(edges, 'start', [], set(), not part2)
    return count


def part2(edges):
    return part1(edges, True)


from aocd import data
runAll(sample, data, parse, part1, part2, answer1, answer2)