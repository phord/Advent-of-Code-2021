#!/bin/python3

from core.skel import *

sample="""[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]"""


answer1 = 4140
answer2 = 3993

def isnum(x):
    return x >= '0' and x <= '9'

def findnum(n,x,dir=1):
    while x >= 0 and x < len(n):
        if isnum(n[x]):
            return x
        x += dir
    return None

# x points to the left digit of the pair
def explode(n, x):
    a = int(n[x])
    b = int(n[x+2])

    # add a to first number to left, if any
    apos = findnum(n, x-1, -1)
    if apos is not None:
        n[apos] = str(int(n[apos]) + a)

    # add b to first number to right, if any
    bpos = findnum(n, x+3, 1)
    if bpos is not None:
        n[bpos] = str(int(n[bpos]) + b)

    # Replace found pair with 0
    n[x-1:x+4] = '0'
    return n

# x points to the number > 9
def split(n, x):
    a = int(n[x])
    n[x:x+1] = ['[', str(a//2), ',', str((a+1)//2), ']']
    return n

def reduce1(n):
    depth = 0
    for x in range(len(n)):
        if depth == 5:
            return (explode(n,x), True)
        if n[x] == '[':
            depth += 1
        elif n[x] == ']':
            depth -= 1

    for x in range(len(n)):
        if isnum(n[x]) and int(n[x]) > 9:
            return (split(n,x), True)

    return (n, False)

def reduce(n):
    changed = True
    while changed:
        n, changed = reduce1(n)
    return n

def add(a, b):
    nn = [x for x in '[a,b]']
    nn[3:4] = b
    nn[1:2] = a
    return reduce(nn)

def extract(n):
    depth = 0
    for x in range(len(n)):
        if n[x] == '[':
            depth += 1
        elif n[x] == ']':
            depth -= 1
        if depth == 0:
            return n[:x+1]
    return n  # err?

def pair(n):
    a = extract(n)
    b = extract(n[len(a)+1:])

    return (a,b)

def mag(n):
    if isnum(n[0]):
        return int(n[0])

    a,b = pair(n[1:])
    return 3*mag(a) + 2*mag(b)

def parse(input):
    lines = [[a for a in x] for x in input.splitlines() if x]
    return lines

def part1(input, part2=False):
    result = input[0]
    for num in input[1:]:
        result = add(result, num)

    return mag(result)


def part2(input):
    biggest = 0
    for a in input:
        for b in input:
            if str(a) != str(b):
                biggest = max(biggest, mag(add(a,b)))
    return biggest


from aocd import data
runAll(sample, data, parse, part1, part2, answer1, answer2)