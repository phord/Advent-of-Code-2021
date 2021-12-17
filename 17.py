#!/bin/python3

from core.skel import *

sample = """
target area: x=20..30, y=-10..-5
"""
answer1 = None
answer2 = None

pascal = []
total = 0
for x in range(10000):
    total += x
    pascal.append(total)

def parse(input):
    lines = [[int(a) for a in parse_fields(x,digits+'-')] for x in input.splitlines() if x][0]
    return lines

def track_probe(pos, vel):
    dx, dy = vel
    x,y = pos
    x += dx
    y += dy
    dx -= sign(dx)
    dy -= 1
    return ((x,y), (dx, dy))

def on_target(pos, target):
    x1, x2, y1, y2 = target
    x,y = pos
    return (x1 <= x <= x2 or x1 >= x >= x2) and (y1 <= y <= y2 or y1 >= y >= y2)

def will_hit(target, vel):
    x1, x2, y1, y2 = target
    dx, dy = vel

    # all the y positions
    y = 0
    x = 1
    t = []
    while dy > 0 or y >= y1:
        y += dy
        dy -= 1
        if y1 <= y <= y2:
            t.append(x)

    # all the x positions when y is in range
    px = [dx * t0 - pascal[t0-1] for t0 in t if t0 <= dx+1]

    # if vel[0] in [6,7]:
    #     print(vel, t, py)
    return any([x1<= p <= x2 for p in px])

def trial(input, vel):
    best = 0
    pos = (0,0)
    x1, x2, y1, y2 = input
    ivel = vel
    while vel[1] > 0 or pos[1] >= min(input[2:]):
        pos, vel = track_probe(pos, vel)

        # if ivel[0] == 10:
        #     print(f"TRACKING  {pos}")

        # if vel[0] == 0:
        #     # We're going to miss
        #     if not (x1 <= pos[0] <= x2 or x1 >= pos[0] >= x2):
        #         break

        best = max([best, pos[1]])
        # print(f"Step {x}: pos={pos}")
        if on_target(pos, input):
            print(f"BULLSEYE {ivel}  {pos}  {best}")
            return best, pos
    # if ivel[0] == 10:
    #     print(f"MISS {ivel}  {best}")
    return -1, pos

def part1(input, part2=False):
    return None
    pos = (0,0)
    vel = (7,2)
    vel = (6,3)

    X = max(input[:2])
    Y = min(input[2:])

    vels = set()
    pos = ()
    best = 0
    while X > 0:
        print(f"{X},{Y}: {best}")

        # increase y until we hit
        y = Y
        while y < 500:
            test, pos = trial(input, (X,y))
            # print(f" look for hit {X},{y}: {pos} {best}")

            # if pos[0] < input[0]:
            #     # No longer reaching the target
            #     print(f"----- MISS TARGET --- {pos}")
            #     return (best, len(vels))

            if test >= 0:
                best = max(best, test)
                vels.add((X,y))
                break

            y += 1

        # Increase y until we miss
        while y < 500:
            y += 1
            test, pos = trial(input, (X,y))
            # print(f" look for miss {X},{y}: {pos} {best}")
            if test >= 0:
                best = max(best, test)
                vels.add((X,y))
            else:
                break
        X -= 1

    a = list(vels)
    a.sort()
    print(a)
    return (best, len(vels))


def part2(input):
    pos = (0,0)

    X = max(input[:2])
    Y = min(input[2:])

    vels = set()
    for x in range(X,0,-1):
        for y in range(Y,100):
            if will_hit(input, (x,y)):
                # print(x,y)
                vels.add((x,y))

    # a = list(vels)
    # a.sort()
    # print(a)
    return len(vels)

from aocd import data
runAll(sample, data, parse, part1, part2, answer1, answer2)