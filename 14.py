#!/bin/python3

from core.skel import *
from collections import defaultdict

sample = """
NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C
"""
answer1 = 1588
answer2 = 2188189693529

def parse(input):
    lines = [parse_fields(x,digits+alpha) for x in input.splitlines() if x]
    start = lines[0]
    rules = {x[0]:x[1] for x in lines[1:]}
    return (start, rules)

def part1(input, part2=False):
    start, rules = input
    start = start[0]

    count = defaultdict(int)
    pairs = defaultdict(int)

    for x in range(len(start)-1):
        pair = start[x:x+2]
        count[start[x]] += 1
        pairs[pair] += 1
        # print(f"{pair} {len(count)} {len(pairs)}")

    count[start[-1]] += 1

    for step in range(40 if part2 else 10):
        p2 = dict(pairs)
        for pair in p2:
            if pair in rules:
                cp = p2[pair]
                ch = rules[pair]
                x,y = pair
                pairs[x + ch] += cp
                pairs[ch + y] += cp
                pairs[pair] -= cp
                count[ch] += cp

    emax = max(count.values())
    emin = min(count.values())
    return emax - emin


def part2(input):
    return part1(input, True)



from aocd import data
runAll(sample, data, parse, part1, part2, answer1, answer2)