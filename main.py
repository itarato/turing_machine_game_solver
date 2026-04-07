from typing import Callable

from lib.common import *
from lib.rules import *
from lib.solver import *


if __name__ == "__main__":
    solver = Solver(341)
    MidpointOrdering(DIGIT_BLUE, 3).analyze(solver, 332)
    # [311, 312, 313, 314, 315, 321, 322, 323, 324, 325, 331, 332, 333, 334, 335, 341, 342, 343, 344, 345, 351, 352, 353, 354, 355]
    print(solver.available)
    EvenOdd(DIGIT_PURPLE).analyze(solver, 344)
    # [311, 313, 315, 321, 323, 325, 331, 333, 335, 341, 343, 345, 351, 353, 355]
    print(solver.available)
    DigitOrdering(DIGIT_BLUE, DIGIT_YELLOW).analyze(solver, 213)
    # [331, 333, 335, 341, 343, 345, 351, 353, 355]
    print(solver.available)
    DigitOrdering(DIGIT_BLUE, DIGIT_YELLOW).analyze(solver, 113)
    # [341, 343, 345, 351, 353, 355]
    print(solver.available)
    MidpointOrdering(DIGIT_PURPLE, 1).analyze(solver, 331)
    # [341, 351]
    print(solver.available)
