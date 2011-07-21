#! /usr/bin/python
 

import unittest
from glicko_algo import *


class TestGlickoAlgo(unittest.TestCase):

    def setUp(self):
        self.player = Player(1500.0, 200.0)
        self.opponent_1 = Player(1400.0, 30.0)
        self.opponent_2 = Player(1550.0, 100.0)
        self.opponent_3 = Player(1700.0, 300)
        self.opponents = (
                        self.opponent_1, 
                        self.opponent_2, 
                        self.opponent_3
                        )

    def test_abs_diff(self):
        result = g_func(self.opponent_1.rating_deviation)
        self.assertAlmostEqual(result, .9955, places=3)

        result = g_func(self.opponent_2.rating_deviation)
        self.assertAlmostEqual(result, .9531, places=3)

    def test_expected_outcome(self):
        expected_outcome_opponent_1 = expected_outcome_given_ratings(
                                   1500,
                                   self.opponent_1.rating,
                                   self.opponent_1.rating_deviation)

        self.assertAlmostEqual(expected_outcome_opponent_1,
                               .639,
                               places=3)
        
        expected_outcome_opponent_3 = expected_outcome_given_ratings(
                                    1500,
                                    self.opponent_3.rating,
                                    self.opponent_3.rating_deviation
                                    )

        self.assertAlmostEqual(expected_outcome_opponent_3, 
                               .303, 
                               places=3)

    def test_d_squared(self):
        d_squared = dd(self.player, self.opponents)

        self.assertAlmostEqual(d_squared, 53670.85, places=-3)

    def test_post_period_rating(self):

        make_match = lambda item : {'opponent': item[0],
                                                    'result': item[1]}

        matches = map(make_match, zip(self.opponents, (1, 0, 0)))

        post_rating = post_period_rating(self.player, matches)

        self.assertAlmostEquals(post_rating, 1464.0, places=0)

if __name__ == '__main__':
    unittest.main()
