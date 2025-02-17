#!/usr/bin/env python3.10

import unittest
from solution import *

class TestAll(unittest.TestCase):

    def test_solve(self):
        self.assertEqual(solve(1, "example1"), 2)
        self.assertEqual(solve(1, "input1"), 655)
        self.assertEqual(solve(2, "example2"), 1)
        self.assertEqual(solve(2, "input2"), 673)

if __name__ == "__main__":
    unittest.main(failfast=True)
