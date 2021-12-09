#!/bin/python3

from core.skel import *

# Weird puzzle had two sets of inputs; Fucked up my pattern.  Oh, well.

sample = """
be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce
"""

# sample="""acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf
# """
answer1 = 26
answer2 = None

# Map display segments to actual digit represented
# Signals are sorted for easy lookup
sigs = {
    "cf" : 1,

    "acf" : 7,

    "bcdf" : 4,

    "acdeg" : 2,
    "acdfg" : 3,
    "abdfg" : 5,

    "abcefg" : 0,
    "abdefg" : 6,
    "abcdfg" : 9,

    "abcdefg" : 8,
}


def parse(input):
    lines = [parse_fields(x,digits+alpha) for x in input.splitlines() if x]
    return lines

allpins = set('abcdefg')

# Init possible pin mappings. Each pin can map to any pin, including itself.
def init():
    pins = {}
    for x in allpins:
        pins[x] = set(allpins)
    return pins

# Remove dest from possible mappings for pin src
# For convience to callers, dest is a set or a string
def elim(pins, src, dest):
    pins[src] -= set(dest)
    if len(pins[src]) == 1:
        pins = assign(pins, src, pins[src])
    return pins

# assign a pin mapping. Remove the dest pin from any other mappings
# For convience to callers, dest is a one-element set or a single-letter string
def assign(pins, src, dest):
    assert len(dest) == 1
    pins[src] = dest
    for x in allpins:
        if x != src:
            if dest < pins[x]:
                pins = elim(pins, x, dest)
    return pins

# pins in src map to pins in dest
def reduce(pins, src, dest):
    assert len(src) == len(dest)

    # Eliminate dest pins from all the pins not in src
    for x in allpins - set(src):
        pins = elim(pins, x, dest)

    # Eliminate any pin mappings in src that don't go to pins in dest
    # If this solves any pin, "assign" it so it gets eliminated from all others
    for x in set(src):
        pins[x] = pins[x].intersection(set(dest))
        if len(pins[x]) == 1:
            pins = assign(pins, x, pins[x])
    return pins

# Decode the mixed-up signals into correct signals and sort the results for easy lookup
def remap(pins, sigs):
    actual = sorted([list(pins[x])[0] for x in sigs])
    return ''.join(actual)

# Reverse the pins mapping from "good => bad" to "bad => good"
# Assumes all unknowns have been solved
def invert(pins):
    assert solved(pins)
    p2 = {list(v)[0]: k for k,v in pins.items()}
    return p2

# Returns true if every pin has exactly one solution
def solved(pins):
    return all([len(x) == 1 for x in pins.values()])

# Find some of the numbers and deduce the pin mappings
def decode(line):
    pins = init()
    # 7
    acf = set([x for x in line if len(x) == 3][0])
    pins = reduce(pins, 'acf', acf)

    # 1
    cf = set([x for x in line if len(x) == 2][0])
    pins = reduce(pins, 'cf', cf)
    assert len(pins['a']) == 1

    # 4
    bcdf = [x for x in line if len(x) == 4][0]
    pins = reduce(pins, 'bcdf', bcdf)

    # 3 (only 5-pin that contains "seven")
    acdfg = [x for x in line if len(x) == 5  and set(x) > set(acf)][0]
    pins = reduce(pins, 'acdfg', acdfg)

    # 9 (6-pin that contains "four")
    abcdfg = set([x for x in line if len(x) == 6 and set(x) > set(bcdf)][0])
    pins = reduce(pins, 'abcdfg', abcdfg)
    assert len(pins['g']) == 1

    # 6 (6-pin that contains exactly half of "one")
    abdefg = set([x for x in line if len(x) == 6 and len(set(x).intersection(cf)) == 1][0])
    pins = reduce(pins, 'abdefg', abdefg)
    assert len(pins['c']) == 1
    assert len(pins['f']) == 1

    assert solved(pins)
    return pins

def part1(input, part2=False):
    count = 0
    for line in input:
        l = [len(x) for x in line]
        patt = [x for x in line[10:] if len(x) in (2,3,4,7)]
        count += len(patt)
    return count


def part2(input):
    total = 0
    for line in input:
        pins = decode(line)
        pins = invert(pins)
        output = 0
        for digit in line[10:]:
            actual = remap(pins, digit)
            assert actual in sigs
            output = output*10 + sigs[actual]
        total += output
    return total


from aocd import data
runAll(sample, data, parse, part1, part2, answer1, answer2)