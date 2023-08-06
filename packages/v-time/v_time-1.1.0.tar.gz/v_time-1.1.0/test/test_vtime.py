"""
    Tests for v_time.py
"""

import unittest
import logging
from time import sleep

import v_time


class TestVTime(unittest.TestCase):
    """Test v_time"""

    def test_timeit(self):
        """ Test the timeit function """

        dummy_function = lambda x: x + 2

        @v_time.timeit
        def timeit_function(x):
            return dummy_function(x)

        self.assertEqual(dummy_function(42), timeit_function(42))

    def test_stimeit(self):
        """ Test the stimeit function """

        dummy_function = lambda x: x + 2

        @v_time.stimeit(logging.info)
        def stimeit_function(x):
            return dummy_function(x)

        self.assertEqual(dummy_function(42), stimeit_function(42))

    def test_mesure(self):
        """ Test the stimeit function """

        num_tests = 10
        sleep_time = 0.1

        out = v_time.mesure(sleep, sleep_time, n_iterations=num_tests)

        self.assertEqual(len(out), num_tests)

        # n times 1 second should be between 9 and 11
        self.assertTrue((num_tests - 1) * sleep_time <= sum(out) <= (num_tests + 1) * sleep_time)

    def test_time_human(self):
        """ Test get time_human function """

        data = [
            (58, "58.00 s"),
            (90, "1.50 min"),
            (3600, "1.00 h"),
            (3600 * 24, "1.00 days"),
            (3600 * 24 * 365, "1.00 years"),
        ]

        for value, result in data:
            self.assertEqual(v_time.time_human(value), result)
