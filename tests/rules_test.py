import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from lib.rules import *


class RulesTest(unittest.TestCase):
    def test_1(self):
        self.assertEqual(
            RULES[1].computation(231),
            ORD_GT,
        )


if __name__ == "__main__":
    unittest.main()
