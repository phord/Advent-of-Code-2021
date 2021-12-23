#!/bin/python3

from core.skel import *
from functools import lru_cache

sample = "xxx"
#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########
answer1 = None
answer2 = None

#
# 89012345678
#   4 5 6 7
#   0 1 2 3
#
room = [(0,4), (1,5), (2,6), (3,7)]
# room = tuple(range(8))
parking = (8,9,11,13,15,17,18)
# paths = {
#     0: (4),
#     1: (5),
#     2: (6),
#     3: (7),
#     4: (0,10),
#     5: (1,12),
#     6: (2,14),
#     7: (3,16),
#     9: (8,10),
#     10: (4,9,11),
#     11: (10,12),
#     12: (5,11,13),
#     13: (14,12),
#     14: (6,13,15),
#     15: (14,16),
#     16: (7,15,17),
#     17: (16,18),
#     18: (17),
# }

entrance = { ##       Hallway to room transition
    0:  10,
    1:  12,
    2:  14,
    3:  16,
    4:  10,
    5:  12,
    6:  14,
    7:  16
}

paths = { ##       Distance to parking      HEAD
    0:  (parking, (4,  3, 3, 5, 7, 9, 10),   10 ),
    1:  (parking, (6,  5, 3, 3, 5, 7,  8),   12 ),
    2:  (parking, (8,  7, 5, 3, 3, 5,  6),   14 ),
    3:  (parking, (10, 9, 7, 5, 3, 3,  4),   16 ),
    4:  (parking, (3,  2, 2, 4, 6, 8,  9),   10 ),
    5:  (parking, (5,  4, 2, 2, 4, 6,  7),   12 ),
    6:  (parking, (7,  6, 4, 2, 2, 4,  5),   14 ),
    7:  (parking, (9,  8, 6, 4, 2, 2,  3),   16 ),
    #              Distance to rooms 0..7
    8:  (room,    (4, 6, 8, 10, 3, 5, 7, 9)),
    9:  (room,    (3, 5, 7,  9, 2, 4, 6, 8)),
    # 10: (room,    ()),
    11: (room,    (3, 3, 5,  7, 2, 2, 4, 6)),
    # 12: (room,    ()),
    13: (room,    (5, 3, 3,  5, 4, 2, 2, 5)),
    # 14: (room,    ()),
    15: (room,    (7, 5, 3, 3,  6, 4, 2, 2)),
    # 16: (room,    ()),
    17: (room,    (9, 7, 5, 3,  8, 6, 4, 2)),
    18: (room,   (10, 8, 6, 4,  9, 7, 5, 3)),
}

#############
#...........#
###B#C#B#D###
# #A#D#C#A#
# #########
#         A, A, B, B, C, C, D, D
sample_data = [0, 3, 4, 6, 5, 2, 1, 7]

#############
#...........#
###B#B#C#D###
#  D#A#A#C#
#  ########
#         A, A, B, B, C, C, D, D
real_data  = [1, 2, 4, 5, 3, 6, 0, 7]
energy = [10**(x//2) for x in range(8)]

def parse(input):
    # if input == 'xxx':
    #     return sample_data
    return real_data

# There are 7 parking spots in the hallway where a pod can rest.
# There are 4 places in the hallway they cannot rest.
# A pod will only move from the room to the hallway and stop, or from the hallway to their final destination.
# A pod will not move into a room unless it contains only other target-correct pods.
# Energy required: A: 1, B: 10, C: 100, D: 1000
#


def all_clear(data, dest, head):
    clear = range(dest, head+1) if head > dest else range(head, dest+1)
    blockers = set(data).intersection(set(clear))
    return not blockers

def clear_to_go_home(data, dest, head):
    clear = range(dest+1, head+1) if head > dest else range(head, dest)
    blockers = set(data).intersection(set(clear))
    return not blockers

def can_go_home(data, pod):
    pos = data[pod]
    pair_pos = data[pod ^ 1]        # position of our partner
    goal = room[pod//2]

    # Pod is in a room
    if pos < 8:
        return False

    # Pod is in the hallway
    dests = set(goal) - set(data)
    if not dests:
        # We can't go anywhere yet
        return False
    elif len(dests) < 2 and pair_pos != goal[0]:
        # Stranger in our room. Can't go home yet
        return False
    else:
        dest = min(dests)
        head = paths[dest][2]
        if all_clear(data, pos, head):
            return True

# Return all the valid moves for given pod
def moves(data, pod):
    pos = data[pod]
    pair_pos = data[pod ^ 1]        # position of our partner
    goal = room[pod//2]

    # Pod is in a room
    if pos < 8:
        if pos in goal and (pos < 4 or pair_pos in goal):
            # We are done
            # print(f"{pos} is home")
            return
        elif pos < 4 and pos + 4 in data:
            # Someone is blocking our way
            # print(f"{pos} can't leave the room")
            return
        else:
            # Move to parking place in hallway
            targets, distance, head = paths[pos]
            for dest, dist in [(dest, dist) for dest, dist in zip(targets, distance) if all_clear(data, dest, head)]:
                yield (dest, dist)

    # Pod is in the hallway already
    else:
        dests = set(goal) - set(data)
        if not dests:
            # print(f"{pos} room is full")
            # We can't go anywhere yet
            return
        elif len(dests) < 2 and pair_pos != goal[0]:
            # Stranger in our room. Can't go home yet
            # print(f"{pos} room is occupied")
            return
        else:
            dest = min(dests)
            distance = paths[pos][1]
            head = paths[dest][2]
            if clear_to_go_home(data, pos, head):
                dist = distance[dest]
                yield (dest, dist)
            else:
                # print(f"{pos} path is blocked {data} {pos} {head}")
                return


def solved(data):
    return all([x in room[pod//2] for pod, x in enumerate(data)])

def dump(data):
    d = set(data)
    revd = ['.']*19
    for pod, pos in enumerate(data):
        revd[pos] = chr(65+pod//2)
    hallway = ''.join(revd[8:])
    rm1 = '#'.join(revd[4:8])
    rm2 = '#'.join(revd[0:4])
    print(f"""#############
#{hallway}#
###{rm1}###
  #{rm2}#
  #########""")

@lru_cache(maxsize=None)
def estimate_energy_needed(data):
    E = 0
    for pod in range(8):
        pos = data[pod]
        pair_pos = data[pod ^ 1]        # position of our partner
        goal = room[pod//2]

        # Pod is in a room
        if pos < 8:
            if pos in goal and (pos < 4 or pair_pos in goal):
                # We are done
                # print(f"{pos} is home")
                continue
            # elif pos < 4 and pos + 4 in data:
            #     # Someone is blocking our way
            #     # print(f"{pos} can't leave the room")
            #     return
            else:
                # Move to parking place in hallway
                targets, distance, head = paths[pos]
                dist, pos = min([(dist, dest) for dest, dist in zip(targets, distance)])
                E += dist * energy[pod]

        # Pod is now in the hallway (hypothetically)
        dest = max(goal)
        distance = paths[pos][1]
        dist = distance[dest]
        E += dist * energy[pod]

    # E should already be a very liberal estimate, on the low side.  But we're missing opportunities somehow.
    return max(0, E - 1200)

solutions = []
def solve(data, path):
    # Recursed too far
    if (len(path[1]) > 500):
        return

    if solutions:
        upper_bound = solutions[-1][0]
        E = estimate_energy_needed(data)
        if upper_bound < path[0] + E:
            print(upper_bound, E, data)    ## Optimistic solution cost
            return


    print(data, path[0], [x[1] for x in path[1]] )
    if solved(data):
        solutions.append(path)
        return

    # canmove = True
    # while canmove:
    #     canmove = False
    gohome = set([pod for pod in range(8) if can_go_home(data, pod)])

    best_home  = sorted([(distance, destination, pod) for pod in gohome for destination, distance in moves(data, pod)])
    best_hallway  = sorted([(distance, destination, pod) for pod in set(range(8)) - gohome for destination, distance in moves(data, pod)])
    best = best_home
    best.extend(best_hallway)
    expense, path = path
    # if not best:
        # print(" NO MORE MOVES   "*5)
    for distance, destination, pod in best:
        e = distance * energy[pod]
        d = list(data)
        p = path[:]
        p.append((pod, data[pod], destination, e))
        # print(f"Move {d[pod]} -> {destination}")
        d[pod] = destination
        # dump(d)
        solve(tuple(d), (expense + e, p))

def part1(data, part2=False):
    solutions = []
    solve(tuple(data), (0, []))
    print(len(solutions), min(solutions))
    return min(solutions)[0]


def part2(input):
    return None
    return part1(input, True)


from aocd import data
runAll(sample, data, parse, part1, part2, answer1, answer2)