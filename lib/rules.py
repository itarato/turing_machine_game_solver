from lib.common import *
from lib.solver import *


class Rule:
    def __init__(self):
        pass

    #
    # The eval computation of the card.
    #
    def computation(self, value: int) -> int:
        raise NotImplementedError

    #
    # The main entrypoint to analyse a guess.
    #
    def analyze(self, solver: Solver, guess: int):
        secret_result = self.computation(solver.secret)
        guess_result = self.computation(guess)
        result_match = secret_result == guess_result
        eliminate(
            solver.available,
            lambda n: (self.computation(n) == guess_result) ^ result_match,
        )


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

    def computation(self, value) -> int:
        return comp(digit_value(value, self.digit), self.midpoint)


# Card 1
# To pass the test of this Verifier, you must find if the
# number is equal to or greater than 1.
# Watch out! If the number in your proposal is 3 and you
# get a this does NOT mean that the number is 3, it
# only means that it must be greater than 1 (and not equal to it).
class LeftPointOrdering(MidpointOrdering):
    def __init__(self, digit: int):
        super().__init__(digit, 1)


# Cards 5 to 7
# To pass this test, find if the number has to be even
# (2 or 4) or odd (1, 3, or 5).
class EvenOdd(Rule):
    def __init__(self, digit: int):
        super().__init__()
        self.digit = digit

    def computation(self, value):
        return digit_value(value, self.digit) % 2


# Cards 8 to 10
# The Verifier verifies that there is a precise number (that they
# know) of 1s in your proposal. For example, they can verify
# that there are two (no more, no less). In this case, the code
# can be 113, 151, 411, etc.
class NumberOrDigits(Rule):
    def __init__(self, n: int):
        super().__init__()
        self.n = n

    def computation(self, value):
        return digit_list(value).count(self.n)


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

    def computation(self, value):
        return comp(
            digit_value(value, self.digit_lhs),
            digit_value(value, self.digit_rhs),
        )


# Cards 14 to 15
# The Verifier verifies that the number of a particular colour
# (that they know) is smaller than all the other numbers.
class TwoDigitOrdering(Rule):
    def __init__(self, smallest_digit: int):
        super().__init__()
        self.smallest_digit = smallest_digit

    def computation(self, value):
        digival = digit_value(value, self.smallest_digit)
        other_digival1 = digit_value(value, (self.smallest_digit + 1) % 3)
        other_digival2 = digit_value(value, (self.smallest_digit + 2) % 3)
        return digival < other_digival1 and digival < other_digival2


# Card 16
# The Verifier verifies that there are more of either even
# (e.g.: 454) or odd (e.g.: 341) numbers in the code.
class MoreEvenOrOdd(Rule):
    def computation(self, value):
        digivals = digit_list(value)
        evens = list(map(lambda x: x % 2, digivals)).count(0)
        odds = list(map(lambda x: x % 2, digivals)).count(0)
        return evens < odds


# Card 17
# The Verifier verifies that there is a precise number
# (that they know) of even numbers in the code:
# zero, one, two, or three.
class EvenCount(Rule):
    def computation(self, value):
        digivals = digit_list(value)
        return list(map(lambda x: x % 2, digivals)).count(0)


# Card 18
# The Verifier verifies that the sum of all the numbers in the code
# is either even or odd.
class SumParity(Rule):
    def computation(self, value):
        return sum(digit_list(value)) % 2


# Card 19
# These cards work like cards 2 to 4, but the Verifier compares
# the sum of the and numbers to 6. This sum can be less than,
# equal to, or greater than 6.
class BlueYellowSumToSix(Rule):
    def computation(self, value):
        blue = digit_value(value, DIGIT_BLUE)
        yellow = digit_value(value, DIGIT_YELLOW)
        return comp(blue + yellow, 6)


# Card 20
# The Verifier verifies if a number repeats itself, and if it so, how many
# times. There may be no repetition (e.g.: 125), one number repeats
# itself once (e.g.: 121), or a number repeats itself twice (e.g.: 222).
# If a number repeats itself, the Verifier does not know anything about it.
# They don’t know the colour (if it’s ) or its number (a 2 or a 3, etc,).
class Repetition(Rule):
    def computation(self, value):
        return super().computation(value)
