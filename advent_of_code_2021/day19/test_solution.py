#!/usr/bin/env python3

import unittest
from solution import *

class TestAll(unittest.TestCase):

    def test_transform(self):
        return
        data = [[1, 2, 3], [4, 5, 6]]
        for thing in transform(data):
            print(thing)

    def test_solve(self):
        self.assertEqual(solve(1, "example"), 79)
        self.assertEqual(solve(1, "input"), -1)
        self.assertEqual(solve(2, "example"), 2)
        self.assertEqual(solve(2, "input"), 2)

if __name__ == "__main__":
    unittest.main()
