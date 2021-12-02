#!/bin/python3

sample = """
"""

def parse(input):
    lines = [x.split() for x in input.splitlines() if x]
    return lines

def part1(input):
    return None


def part2(input):
    return None


## ===================================================

from colorama import Fore, Style

def runAll(sample, actual):
    CYAN = Fore.CYAN
    GREEN = Fore.GREEN
    YELLOW = Fore.YELLOW
    RED = Fore.RED
    RESET = Style.RESET_ALL

    sample = parse(sample)
    actual = parse(actual)

    print(f"{CYAN}Parse:")
    print(f"  {sample}{RESET}")
    print()
    print(f"""{YELLOW}Sample:{RED}""")
    p1 = part1(sample)
    print(f"{YELLOW}  Part 1: {p1}{RED}")
    p2 = part2(sample)
    if p2 is not None:
        print(f"{YELLOW}  Part 2: {p2}{RED}")
    print()
    print(f"""{GREEN}Actual:{RED}""")
    p1 = part1(actual)
    print(f"{GREEN}  Part 1: {p1}{RED}")
    p2 = part2(actual)
    if p2 is not None:
        print(f"{GREEN}  Part 2: {p2}{RESET}")


actual = """
"""

runAll(sample, actual)