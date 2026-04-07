from typing import Callable

from lib.common import *
from lib.rules import *
from lib.solver import *


if __name__ == "__main__":
    solver = Solver(341)
    MidpointOrdering(DIGIT_BLUE, 3).analyze(solver, 332)
    print(solver.available)
