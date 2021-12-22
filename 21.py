#!/bin/python3

from functools import lru_cache

# Each time we call play, it is player1's turn.  (We swap them on each call.)
@lru_cache(maxsize=None)
def play(pos1, pos2, score1, score2):
    # Player2 just moved.  See if he won.
    if score2 >= 21:
        return [0, 1]

    wins1 = 0
    wins2 = 0
    for die1 in range(1,4):
        for die2 in range(1,4):
            for die3 in range(1,4):
                newpos = (pos1 + die1 + die2 + die3 - 1) % 10 + 1
                w1, w2 = play(pos2, newpos, score2, score1 + newpos)
                wins1 += w1
                wins2 += w2

    # swap the wins when we return
    return [wins2, wins1]

start_pos = [4,2]  # My input
wins = play(*start_pos, 0, 0)
print(f"Answer={max(wins)}")
