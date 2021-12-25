#!/bin/python3

from core.skel import *
import random

sample = """
inp w
mul x 0
add x z
mod x 26
div z 1
add x 14
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 12
mul y x
add z y
"""
answer1 = None
answer2 = None

def parse(input):
    lines = [x.split(' ') for x in input.splitlines() if x]
    return lines

def run(program, stdin):
    reg = {"w": 0, "x": 0, "y": 0, "z": 0, }

    prev = 0
    print(f"==== INPUT: {''.join([x for x in stdin])} ====")
    line = 1
    for op in program:
        var = op[1]
        if op[0] == 'inp':
            reg[var] = int(stdin[0])
            stdin = stdin[1:]
        else:
            operand = reg[op[2]] if str(op[2]) in 'wxyz' else int(op[2])
            if op[0] == 'add':
                reg[var] += operand
            elif op[0] == 'mul':
                reg[var] *= operand
            elif op[0] == 'div':
                reg[var] //= operand
            elif op[0] == 'mod':
                reg[var] %= operand
            elif op[0] == 'eql':
                reg[var] = 1 if reg[var] == operand else 0

        print(line, ' '.join([str(x) for x in op]), "   ", ' '.join([f"{var}={reg[var]}" for var in reg]))
        line += 1
    return reg['z']

def part1(input):

    ## 14 digits have a palindrom relationship (7 each)
    ## 1  2  3  4  5  6  7  8  9 10 11 12 13 14
    ##       ====
    ##                   ====  d8 = d7-1
    ##                         ====  d10 = d9+2
    ##                =================  d11 = d6+3
    ##             =======================  d12 = d5-5
    ##             =======================  d13 = d2-7
    ##             =======================  d14 = d1+6

    #      12345678901234
    stdin="39999698799429"
    stdin="18116121134117"

    result = run(input, stdin)
    print (result, input)
    return None


def part2(input):
    return None ## part1(input, True)


from aocd import data
runAll(sample, data, parse, part1, part2, answer1, answer2)