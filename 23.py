#!/bin/python3

from core.skel import *
from functools import lru_cache

sample = "xxx"
#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########

#############
#...........#
###B#C#B#D###
  #D#C#B#A#  <-- Part 2
  #D#B#A#C#  <-- Part 2
  #A#D#C#A#
  #########

answer1 = None
answer2 = None

#
# 89012345678
#   4 5 6 7
#   0 1 2 3
#
room = [tuple(range(x-8,x+8,4)) for x in range(4)]
# room = tuple(range(8))
parking = (8,9,11,13,15,17,18)

#############
#...........#
###B#C#B#D###
  #D#C#B#A#  <-- Part 2
  #D#B#A#C#  <-- Part 2
# #A#D#C#A#
# #########
#              A, A, A, A,  B,   B, B,  B, C, C, C,  C, D,  D, D, D
sample_data = [0, 3, 6, 11, 12, 14, 5, 10, 2, 7, 9, 13, 1, 15, 4, 8]

#############
#...........#
###B#B#C#D###
  #D#C#B#A#  <-- Part 2
  #D#B#A#C#  <-- Part 2
#  D#A#A#C#
#  ########
#              A, A, A, A,  B,   B, B,  B, C, C, C,  C, D,  D, D, D
real_data   = [1, 2, 6, 11, 12, 13, 5, 10, 3, 14, 7, 9, 0, 15, 4, 8]

part2 = [2, 1, 3, 0, 7, 6, 5, 4]

sample_data = [x-8 for x in sample_data]
print(sorted(sample_data))
print(sorted(list(set(sample_data))))
assert len(sample_data) == 16
assert len(set(sample_data)) == 16

real_data = [x-8 for x in real_data]
assert len(real_data) == 16
assert len(set(real_data)) == 16



energy = [10**(x//4) for x in range(16)]

def parse(input):
    if input == 'xxx':
        return sample_data
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
    r = pod - (pod%4)
    pair_pos = [data[p] for p in range(r,r+4) if p != pod]        # position of our partners
    goal = room[pod//4]

    # Pod is in a room
    if pos < 8:
        return False

    # Pod is in the hallway
    dests = set(goal) - set(data)
    if not dests:
        # We can't go anywhere yet
        return False
    elif len(dests) + len(set(pair_pos).intersection(goal)) != 4:
        # Stranger in our room. Can't go home yet
        return False
    else:
        dest = min(dests)
        head = 10 + pod//4*2  # 10, 12, 14, 16
        if all_clear(data, pos, head):
            return True

# Return all the valid moves for given pod
def moves(data, pod):
    pos = data[pod]
    r = pod - (pod%4)
    pair_pos = [data[p] for p in range(r,r+4) if p != pod]        # position of our partners
    goal = room[pod//4]

    # Pod is in a room
    if pos < 8:
        # Who is below me?

        if pos in goal:
            below_me = frozenset(range(pos%4-8,pos,4))
            if len([x for x in pair_pos if x in below_me]) == len(below_me):
                # We are done
                print(f"{pos} is home")
                return
        elif pos < 4 and any([x in data for x in range(pos + 4, 8, 4)]):
            # Someone is blocking our way
            print(f"{pos} can't leave the room")
            return
        else:
            # Move to parking place in hallway
            head = 10 + pod//4*2  # 10, 12, 14, 16
            for dest in [d for d in parking if all_clear(data, d, head)]:
                dist = 4-(pos + 8)//4 + abs(dest-head)
                yield (dest, dist)

    # Pod is in the hallway already
    else:
        dests = set(goal) - (set(data) - set(pair_pos))
        if len(dests) < 4:
            # Stranger in our room. Can't go home yet
            print(f"{pos} room is occupied")
            return
        else:
            dest = min(dests - set(pair_pos))
            head = 10 + pod//4*2  # 10, 12, 14, 16
            if clear_to_go_home(data, pos, head):
                dist = 4-(dest + 8)//4 + abs(pos-head)
                yield (dest, dist)
            else:
                print(f"{pos} path is blocked {data} {pos} {head}")
                return


def solved(data):
    return all([x in room[pod//4] for pod, x in enumerate(data)])

def dump(data):
    d = set(data)
    revd = ['.']*27
    for pod, pos in enumerate(data):
        revd[pos+8] = chr(65+pod//4)
    hallway = ''.join(revd[16:])
    rm1 = '#'.join(revd[12:16])
    rma = '#'.join(revd[8:12])
    rmb = '#'.join(revd[4:8])
    rm2 = '#'.join(revd[0:4])
    print(f"""#############
#{hallway}#
###{rm1}###
  #{rma}#
  #{rmb}#
  #{rm2}#
  #########""")

@lru_cache(maxsize=None)
def estimate_energy_needed(data):
    E = 0
    for pod in range(16):
        pos = data[pod]
        r = pod - (pod%4)
        pair_pos = [data[p] for p in range(r,r+4) if p != pod]        # position of our partners
        goal = room[pod//4]
        head = 10 + pod//4*2  # 10, 12, 14, 16

        # TODO: Detect deadlock?  We want to move to park, but all paths are blocked.
        #       Or B and C are parked but need to swap places (in a way that can never happen)

        # Pod is in a room
        if pos < 8:
            if pos in goal:
                below_me = frozenset(range(pos%4-8,pos,4))
                if len([x for x in pair_pos if x in below_me]) == len(below_me):
                    # We are done
                    # print(f"{pos} is home")
                    continue
            # elif pos < 4 and any([x in data for x in range(pos + 4, 8, 4)]):
            #     # Someone is blocking our way
            #     print(f"{pos} can't leave the room")
            #     return
            else:
                # Move to parking place in hallway
                dist = 4-(pos + 8)//4 + 1  # Minimum distance to park
                E += dist * energy[pod]
                pos = head + 1

        # Pod is now in the hallway (hypothetically)
        dist = abs(pos-head) + 1   # Minimum distance.  TODO: Add 1 for every pair_pos in parking.
        E += dist * energy[pod]

    # E should already be a very liberal estimate, on the low side.  But we're missing opportunities somehow.
    return max(0, E - 1200)

class Game:
    def __init__(self, data, E=0):
        self.data = tuple(data)
        self.energy = E
        self.dead = False
        self.estimate = estimate_energy_needed(self.data) + E

        if solved(self.data):
            if not solutions or self.energy < min(solutions):
                solutions.append(self.energy)
                print(min(solutions), self.data)    ## Lowest score so far
            self.dead = True
        elif solutions:
            upper_bound = min(solutions)
            if upper_bound <= self.energy:
                self.dead = True

    def next(self):
        if self.dead:
            return

        possmoves = [(distance, destination, pod) for pod in set(range(8)) for destination, distance in moves(self.data, pod)]
        for distance, destination, pod in possmoves:
            data = list(self.data)
            data[pod] = destination
            yield Game(data, self.energy + energy[pod] * distance)



solutions = []
def solve(game):

    games = [game]

    depth = 1
    total = 1
    while games:
        print(f"{depth}. {len(games)} / {total}     {min(solutions) if solutions else 0}")
        depth += 1
        next = []
        for game in games:
            next.extend(game.next())
        total = len(next)
        games = sorted(next, key=lambda _: _.estimate)[:225000]

def part1(data, part2=False):
    global solutions
    solutions = []
    # dump(sample_data)
    # dump(real_data)
    solve(Game(data))
    print(len(solutions), min(solutions) if solutions else 0)
    return min(solutions) if solutions else 0


def part2(input):
    return None
    return part1(input, True)


from aocd import data
runAll(sample, data, parse, part1, part2, answer1, answer2)