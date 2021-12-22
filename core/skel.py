#!/bin/python3

from colorama import Fore, Style

digits = "0123456789"
numbers = "+-." + digits
alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

# Returns -1, 0 or 1
def sign(x):
    if not x: return 0
    return -1 if x < 0 else 1

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
                if word[0] in numbers and all([a in '-+'+digits for a in word[1:]]):
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


def runAll(sample, actual, parse, part1, part2, expect1=None, expect2=None):
    CYAN = Fore.CYAN
    GREEN = Fore.GREEN
    YELLOW = Fore.YELLOW
    RED = Fore.RED
    RESET = Style.RESET_ALL

    print(f"{CYAN}Parse:{RED}")
    s = parse(sample)
    if actual.strip():
        parse(actual)

    print(f"{CYAN}  {s}{RESET}")
    print()

    if (sample.strip()):
        print(f"""{YELLOW}Sample:{RED}""")
        p1 = part1(parse(sample))
        valid = ""
        if expect1 is not None:
            valid = f"{GREEN}  CORRECT" if expect1 == p1 else f"{RED}   WRONG WRONG WRONG"
        print(f"{YELLOW}  Part 1: {p1}            {valid}{RED}")
        p2 = part2(parse(sample))
        if p2 is not None:
            valid = ""
            if expect2 is not None:
                valid = f"{GREEN}  CORRECT" if expect2 == p2 else f"{RED}   WRONG WRONG WRONG"
            print(f"{YELLOW}  Part 2: {p2}            {valid}{RED}")
        print()

    if actual.strip():
        print(f"""{GREEN}Actual:{RED}""")
        p1 = part1(parse(actual))
        print(f"{GREEN}  Part 1: {p1}{RED}")
        p2 = part2(parse(actual))
        if p2 is not None:
            print(f"{GREEN}  Part 2: {p2}{RESET}")
