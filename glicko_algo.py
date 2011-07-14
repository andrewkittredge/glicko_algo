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

def abs_diff(val, expected_val, epsilon=.001):
    return abs(val - expected_val) <= epsilon
    

def test():

    player = Player(1500.0, 200.0)
    opponent_1 = Player(1400.0, 30.0)
    opponent_2 = Player(1550.0, 100.0)
    opponent_3 = Player(1700.0, 300)
    opponents = opponent_1, opponent_2, opponent_3

    assert abs_diff(g_func(opponent_1.rating_deviation), .9955)
    assert abs_diff(g_func(opponent_2.rating_deviation), .9531)

    expected_outcome_opponent_1 = expected_outcome_given_ratings(1500,
                                               opponent_1.rating,
                                               opponent_1.rating_deviation)

    assert abs_diff(expected_outcome_opponent_1, .639)

    expected_outcome_opponent_3 = expected_outcome_given_ratings(1500,
                                                opponent_3.rating,
                                                opponent_3.rating_deviation)

    assert abs_diff(expected_outcome_opponent_3, .303)

    d_squared = dd(player, opponents)

    assert abs_diff(d_squared, 53670.85, 20)

    make_match = lambda item : {'opponent': item[0],
                                                'result': item[1]}

    matches = map(make_match, zip(opponents, (1, 0, 0)))

    post_rating = post_period_rating(player, matches)

    assert abs_diff(post_rating, 1464.0, 1.0)
    
if  __name__ == '__main__':
    test()
