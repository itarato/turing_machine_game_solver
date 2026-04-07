from typing import Callable

from lib.common import *
from lib.solver import *


class Rule:
    def __init__(self):
        self.exhausted = False

    def analyze(self, secret: int, guess: int):
        raise NotImplementedError


# Cards 2 to 4
# These cards work in a very similar way to Card #1, but there
# are now 3 possibilities. In Card #2, the number can be
# either less than, equal to, or greater than the number
# indicated.
# Watch out! If the number in your proposal is 2 and you
# get a , this does NOT mean that the number is 2, it
# only means that it must be less than 3.
class MidpointOrdering(Rule):
    def __init__(self, digit: int, midpoint: int):
        super().__init__()
        self.midpoint = midpoint
        self.digit = digit

    def analyze(self, solver: Solver, guess: int):
        secret_digit = digit_value(solver.secret, self.digit)
        guess_digit = digit_value(guess, self.digit)

        secret_ord = comp(secret_digit, self.midpoint)
        guess_ord = comp(guess_digit, self.midpoint)
        ord_match = secret_ord == guess_ord

        eliminator_fn = self.make_eliminator_fn(guess_ord, ord_match)
        eliminate(solver.available, eliminator_fn)

        self.exhausted = True

    def make_eliminator_fn(
        self,
        guess_ord: int,
        ord_match: bool,  # Eg.: False
    ) -> Callable[[int], bool]:
        return (
            lambda n: (comp(digit_value(n, self.digit), self.midpoint) == guess_ord)
            ^ ord_match
        )
