#!/bin/python3

digits = "0123456789"
numbers = "+-." + digits
alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

sample = """
"""

def parse(input):
    lines = [parse_fields(x,digits+alpha) for x in input.splitlines() if x]
    return lines

def part1(input, part2=False):
    return None


def part2(input):
    return part1(input, True)


## ===================================================

from colorama import Fore, Style

# Returns a list of words containing wordchars
# includes "words" of non-wordchars if keep_delim=True
# Converts words made of numbers into integers instead of strings
# parse_fields(" This is   11  tests.  ",digits+alpha) = ["This", "is", 11, "tests"]
def parse_fields(row, wordchars, keep_delim = False):
    f=[]
    word = ''
    delim = ''
    for x in row:
        if x in wordchars:
            if delim and keep_delim:
                f.append(delim)
            delim = ''
            word += x
        else:
            if word:
                if all([a in digits for a in word]):
                    word = int(word)
                f.append(word)
            word = ''
            delim += x

    if delim and keep_delim:
        f.append(delim)
    elif word:
        if all([a in digits for a in word]):
            word = int(word)
        f.append(word)


    return f


def runAll(sample, actual):
    CYAN = Fore.CYAN
    GREEN = Fore.GREEN
    YELLOW = Fore.YELLOW
    RED = Fore.RED
    RESET = Style.RESET_ALL

    print(f"{CYAN}Parse:{RED}")
    s = parse(sample)
    if actual.strip():
        a = parse(actual)

    print(f"{CYAN}  {s}{RESET}")
    print()
    print(f"""{YELLOW}Sample:{RED}""")
    p1 = part1(parse(sample))
    print(f"{YELLOW}  Part 1: {p1}{RED}")
    p2 = part2(parse(sample))
    if p2 is not None:
        print(f"{YELLOW}  Part 2: {p2}{RED}")
    print()
    if actual.strip():
        print(f"""{GREEN}Actual:{RED}""")
        p1 = part1(parse(actual))
        print(f"{GREEN}  Part 1: {p1}{RED}")
        p2 = part2(parse(actual))
        if p2 is not None:
            print(f"{GREEN}  Part 2: {p2}{RESET}")


actual = """
"""

runAll(sample, actual)