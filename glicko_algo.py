#! /usr/bin/python

'''
Implementation of Mark Glickman's Glicko System.

akittredge, July 2011
'''

import math

Q = (math.log(10.0) / 400.0)
QQ = Q ** 2
pi = math.pi
    
def expected_outcome_given_ratings(player_rating, 
                                   other_player_rating, 
                                   other_player_rating_deviation):

    exponent = -g_func(other_player_rating_deviation) * (player_rating - other_player_rating) / 400.0
    ret_val = 1 / (1 + 10 ** exponent)

    return ret_val

def g_func(rating_deviation):
    denominator = math.sqrt(1.0 + 3.0 * QQ * rating_deviation**2.0 / pi**2)
    return 1.0 / denominator

def dd(player, other_players):
    _sum = 0
    for other_player in other_players:
        g_func_val = g_func(other_player.rating_deviation)

        expected_outcome = expected_outcome_given_ratings(player.rating, 
                                            other_player.rating, 
                                            other_player.rating_deviation)

        _sum += g_func_val**2 * expected_outcome * (1 - expected_outcome)
    return 1 / (QQ * _sum)

    
def post_period_rating(player, matches):
    

    d_squared = dd(player, (match['opponent'] for match in matches))

    factor = Q / (1  / player.rating_deviation ** 2 + (1 / d_squared))

    _sum = 0
    for match in matches:
        opponent_rating = match['opponent'].rating
        opponent_rating_deviation = match['opponent'].rating_deviation
        match_result = match['result']
        expected_result = expected_outcome_given_ratings(player.rating, 
                                                 opponent_rating, 
                                                 opponent_rating_deviation)

        g_func_val = g_func(opponent_rating_deviation)
        _sum +=  g_func_val * (match_result - expected_result)


    return player.rating + factor * _sum

class Player(object):
    def __init__(self, rating, rating_deviation):
        self.rating = rating    
        self.rating_deviation = rating_deviation
