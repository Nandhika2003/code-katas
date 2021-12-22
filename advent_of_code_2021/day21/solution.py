#!/usr/bin/env python3

import sys
sys.path.append("..")

from ansi import *
from comp import *

from collections import Counter

ONE, TWO = (0, 1)
ROLL_DISTRIBUTION = {3: 1,  4: 3,  5: 6,  6: 7,  7: 6,  8: 3,  9: 1}

def get_next_position(curr, advance):
    return (curr + advance - 1) % 10 + 1

def encode(pos1, sco1, pos2, sco2, turn):
    return f"{pos1},{sco1}|{pos2},{sco2}|{turn}"
    return f"{pos1},{sco1 if sco1 < 10 else 'W'}|{pos2},{sco2 if sco2 < 10 else 'W'}|{turn}"

def decode(serialized):
    spl = serialized.split("|")
    p1 = spl[0].split(",")
    p2 = spl[1].split(",")
    turn = spl[2]
    return int(p1[0]), int(p1[1]), int(p2[0]), int(p2[1]), int(turn)

def get_losing_score(player_1, player_2):
    position_of_player = [player_1, player_2]
    score_of_player = [0, 0]
    curr_die_val = 0
    rolls = 0
    curr_player = 0

    while score_of_player[ONE] < 1000 and score_of_player[TWO] < 1000:

        next_roll = (3 * curr_die_val) + 6  # (die + 1) + (die + 2) + (die + 3)  ;-)
        position_of_player[curr_player] = get_next_position(position_of_player[curr_player], next_roll)
        score_of_player[curr_player] += position_of_player[curr_player]

        curr_player = ~curr_player
        curr_die_val += 3
        rolls += 3

    return rolls * min(score_of_player)

def get_universes(state, win_cache={}):
    if memo := win_cache.get(state):
        return memo
    p1, s1, p2, s2, current_player = decode(state)
    position_of_player = [p1, p2]
    score_of_player = [s1, s2]
    curr_player = 1
    p1_wins = 0
    p2_wins = 0
    for roll, freq in ROLL_DISTRIBUTION.items():
        if current_player == ONE:
            new_p1 = get_next_position(p1, roll)
            new_s1 = s1 + new_p1
            if new_s1 >= 21:
                p1_wins += freq
            else:
                incr1, incr2 = get_universes(encode(new_p1, new_s1, p2, s2, TWO))
                p1_wins += incr1 * freq
                p2_wins += incr2 * freq
        elif current_player == TWO:
            new_p2 = get_next_position(p2, roll)
            new_s2 = s2 + new_p2
            if new_s2 >= 21:
                p2_wins += freq
            else:
                incr1, incr2 = get_universes(encode(p1, s1, new_p2, new_s2, ONE))
                p1_wins += incr1 * freq
                p2_wins += incr2 * freq
    win_cache[state] = (p1_wins, p2_wins)
    return win_cache[state]

def solve(prob, inputname):

    position_for_player = [int(line[line.index(":") + 2:]) for line in yield_line(inputname)]

    if prob == 1:
        return get_losing_score(position_for_player[ONE], position_for_player[TWO])
    if prob == 2:
        return max(get_universes(f"{position_for_player[ONE]},0|{position_for_player[TWO]},0|{ONE}", {}))
