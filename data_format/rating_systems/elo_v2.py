from math import pow, copysign, floor, ceil
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import pandas as pd
import numpy as np

E_START_RATING = 1400
RATING_SCALE = 480.0
K_FACTOR = 32.0
K_FUNCTION_AMPLIFIER = 10.0
K_FUNCTION_AMPLIFIER_GRADIENT = 63.0
K_FUNCTION_MULTIPLIER = 2.0 * (K_FUNCTION_AMPLIFIER - 1.0)

DELTA_RATING_CAP = 200.0
MIN_MATCHES = 5
RECENT_WEEKS = 130
LATEST_WEEKS = 56
NOW_WEEKS = 12
RECENT_K_GAIN_FACTOR = 2

# K_Factors in case adding league signifigance in future
TB_K_FACTOR = 1
SERVE_RETURN_K_FACTOR = 1
ACE_K_FACTOR = 1
POINT_K_FACTOR = 1
GAME_K_FACTOR = 1
SET_K_FACTOR = 1


def primary_elo(rA, rB, row):
    delta = delta_rating(rA, rB, "N/A")

    rA_new = new_rating(rA, delta, row['tourney_level'], row['tourney_name'], row['round'], int(row['best_of']), "N/A")
    rB_new = new_rating(rB, -delta, row['tourney_level'], row['tourney_name'], row['round'], int(row['best_of']), "N/A")

    return rA_new, rB_new


def base_competing_elo(rA, rB, pct):
    aDelta = delta_rating(rA, rB, "N/A")

    new_delta_a = (aDelta * pct)

    rA_new = new_rating(rA, new_delta_a)
    rB_new = new_rating(rB, -new_delta_a)

    return rA_new, rB_new

def k_factor(level, tourney_name, round, best_of, outcome):
    k = K_FACTOR
    # if "G" == level:
    #     k *= 1.0
    # elif "Tour Finals" in tourney_name:
    #     k *= .9
    # elif "M" in level:
    #     k *= .85
    # elif "Olympics" in tourney_name:
    #     k *= .8
    # elif "A" in level:
    #     k *= .7
    # else:
    #     k *=.65

    # # Match round adjustment is: Final 100%, Semi-Final 90%, Quarter-Final and Round-Robin 85%, Rounds of 16 and 32 80%, Rounds of 64 and 128 75% and For Bronze Medal 95%
    # round_factors = {
    #     "F": 1.0, "BR": 0.95, "SF": 0.90, "QF": 0.85, "R16": 0.80, "R32": 0.80,
    #     "R64": 0.75, "R128": 0.75, "RR": 0.85
    # }

    # k *= round_factors.get(round, .75)
    
    # if best_of < 5:
    #     k *= 0.90

    # # if outcome == "W/O":
    # #     k *= 0.50
    
    return k

def delta_rating(winner_rating, loser_rating, outcome):
    if outcome == "ABD":
        return 0.0
    delta = 1.0 / (1.0 + pow(10.0, (winner_rating - loser_rating) / RATING_SCALE))
    return delta

def new_rating(rating, delta, level=None, tourney_name=None, round=None, best_of=None, outcome=None):
    return rating + cap_delta_rating(k_factor(level, tourney_name, round, best_of, outcome) * delta * k_function(rating))

def cap_delta_rating(delta):
    return copysign(min(abs(delta), DELTA_RATING_CAP), delta)

def k_function(rating):
    return 1.0 + K_FUNCTION_MULTIPLIER / (1.0 + pow(2.0, (rating - E_START_RATING) / K_FUNCTION_AMPLIFIER_GRADIENT))

def elo_win_probability(elo_rating1, elo_rating2):
    return 1.0 / (1.0 + pow(10.0, (elo_rating2 - elo_rating1) / RATING_SCALE))

