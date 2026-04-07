from typing import Callable

from lib.common import *
from lib.solver import *


class Rule:
    def __init__(self):
        pass

    def analyze(self, solver: Solver, guess: int):
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

    def make_eliminator_fn(
        self,
        guess_ord: int,
        ord_match: bool,
    ) -> Callable[[int], bool]:
        return (
            lambda n: (comp(digit_value(n, self.digit), self.midpoint) == guess_ord)
            ^ ord_match
        )


# Cards 5 to 7
# To pass this test, find if the number has to be even
# (2 or 4) or odd (1, 3, or 5).
class EvenOdd(Rule):
    def __init__(self, digit: int):
        super().__init__()
        self.digit = digit

    def analyze(self, solver, guess):
        secret_digit = digit_value(solver.secret, self.digit)
        guess_digit = digit_value(guess, self.digit)

        secret_odd_or_even = secret_digit % 2
        guess_odd_or_even = guess_digit % 2
        odd_or_even_match = secret_odd_or_even == guess_odd_or_even

        eliminator_fn = self.make_eliminator_fn(guess_odd_or_even, odd_or_even_match)
        eliminate(solver.available, eliminator_fn)

    def make_eliminator_fn(
        self,
        guess_odd_or_even: int,
        odd_or_even_match: bool,
    ) -> Callable[[int], bool]:
        return (
            lambda n: (digit_value(n, self.digit) % 2 == guess_odd_or_even)
            ^ odd_or_even_match
        )


# Cards 11 to 13
# These cards work similarly to cards 2 to 4, but instead of
# comparing a number in your proposal to another specific
# number, it is comparing two numbers within your proposal.
# For example, the number with the number.
# Watch out! If you get if your proposal is 3 and 3 ,
# this does NOT mean that the numbers are 3, just that they
# have to be the same.
class DigitOrdering(Rule):
    def __init__(self, digit_lhs: int, digit_rhs: int):
        super().__init__()
        self.digit_lhs = digit_lhs
        self.digit_rhs = digit_rhs

    def analyze(self, solver, guess):
        secret_ord = comp(
            digit_value(solver.secret, self.digit_lhs),
            digit_value(solver.secret, self.digit_rhs),
        )
        guess_ord = comp(
            digit_value(guess, self.digit_lhs),
            digit_value(guess, self.digit_rhs),
        )
        ord_match = secret_ord == guess_ord

        eliminator_fn = self.make_eliminator_fn(guess_ord, ord_match)
        eliminate(solver.available, eliminator_fn)

    def make_eliminator_fn(
        self,
        guess_ord: int,
        ord_match: bool,
    ) -> Callable[[int], bool]:
        return (
            lambda n: (
                comp(
                    digit_value(n, self.digit_lhs),
                    digit_value(n, self.digit_rhs),
                )
                == guess_ord
            )
            ^ ord_match
        )
