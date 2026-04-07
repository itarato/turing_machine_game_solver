import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from lib.common import *
from lib.rules import *
from lib.solver import *


class TestTuringMachineSmoke(unittest.TestCase):
    """Basic smoke tests for Turing Machine Solver"""

    def test_machine_initialization(self):
        solver = Solver(341)

        MidpointOrdering(DIGIT_BLUE, 3).analyze(solver, 332)
        self.assertEqual(
            solver.available,
            [
                311,
                312,
                313,
                314,
                315,
                321,
                322,
                323,
                324,
                325,
                331,
                332,
                333,
                334,
                335,
                341,
                342,
                343,
                344,
                345,
                351,
                352,
                353,
                354,
                355,
            ],
        )

        EvenOdd(DIGIT_PURPLE).analyze(solver, 344)
        self.assertEqual(
            solver.available,
            [311, 313, 315, 321, 323, 325, 331, 333, 335, 341, 343, 345, 351, 353, 355],
        )

        DigitOrdering(DIGIT_BLUE, DIGIT_YELLOW).analyze(solver, 213)
        self.assertEqual(
            solver.available, [331, 333, 335, 341, 343, 345, 351, 353, 355]
        )

        DigitOrdering(DIGIT_BLUE, DIGIT_YELLOW).analyze(solver, 113)
        self.assertEqual(solver.available, [341, 343, 345, 351, 353, 355])

        MidpointOrdering(DIGIT_PURPLE, 1).analyze(solver, 331)
        self.assertEqual(solver.available, [341, 351])

    def test_left_point_ordering_rule(self):
        solver = Solver(123)

        LeftPointOrdering(DIGIT_BLUE).analyze(solver, 223)
        self.assertEqual(
            solver.available,
            [
                111,
                112,
                113,
                114,
                115,
                121,
                122,
                123,
                124,
                125,
                131,
                132,
                133,
                134,
                135,
                141,
                142,
                143,
                144,
                145,
                151,
                152,
                153,
                154,
                155,
            ],
        )

    def test_number_of_digits(self):
        solver = Solver(133)

        NumberOrDigits(3).analyze(solver, 223)
        NumberOrDigits(3).analyze(solver, 221)
        self.assertEqual(
            solver.available,
            [133, 233, 313, 323, 331, 332, 333, 334, 335, 343, 353, 433, 533],
        )


if __name__ == "__main__":
    unittest.main()
