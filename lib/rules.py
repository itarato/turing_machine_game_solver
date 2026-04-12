from __future__ import annotations

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

    def title(self) -> str:
        raise NotImplementedError

    #
    # The main entrypoint to analyse a guess.
    #
    def analyze(self, solver: Solver, guess: int) -> bool:
        secret_result = self.computation(solver.secret)
        guess_result = self.computation(guess)
        result_match = secret_result == guess_result
        eliminate(
            solver.available,
            lambda n: (self.computation(n) == guess_result) ^ result_match,
        )
        return result_match


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

    def title(self) -> str:
        return f"Ordering: {digit_name(self.digit)} < = > {self.midpoint}"


# Card 1
# To pass the test of this Verifier, you must find if the
# number is equal to or greater than 1.
# Watch out! If the number in your proposal is 3 and you
# get a this does NOT mean that the number is 3, it
# only means that it must be greater than 1 (and not equal to it).
class LeftPointOrdering(MidpointOrdering):
    def __init__(self, digit: int):
        super().__init__(digit, 1)

    def title(self) -> str:
        return f"Pertial ordering: {digit_name(self.digit)} < = > 1"


# Cards 5 to 7
# To pass this test, find if the number has to be even
# (2 or 4) or odd (1, 3, or 5).
class EvenOdd(Rule):
    def __init__(self, digit: int):
        super().__init__()
        self.digit = digit

    def computation(self, value):
        return digit_value(value, self.digit) % 2

    def title(self) -> str:
        return f"{digit_name(self.digit)} is even or odd"


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

    def title(self) -> str:
        return f"Number of digits: ___ / _{self.n}_ / {self.n}{self.n}_ / {self.n}{self.n}{self.n}"


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

    def title(self) -> str:
        return f"Digit ordering: {digit_name(self.digit_lhs)} < = > {digit_name(self.digit_rhs)}"


# Cards 14 to 15
# The Verifier verifies that the number of a particular colour
# (that they know) is smaller than all the other numbers.
class SmallestDigit(Rule):
    def computation(self, value):
        digilist = digit_list(value)
        if digilist[0] < digilist[1] and digilist[0] < digilist[2]:
            return 0
        elif digilist[1] < digilist[0] and digilist[1] < digilist[2]:
            return 1
        elif digilist[2] < digilist[1] and digilist[2] < digilist[0]:
            return 2
        else:
            return -1

    def title(self):
        return f"Smallest digit: _ < _ and _"


# Cards 14 to 15
# The Verifier verifies that the number of a particular colour
# (that they know) is smaller than all the other numbers.
class GreatestDigit(Rule):
    def computation(self, value):
        digilist = digit_list(value)
        if digilist[0] > digilist[1] and digilist[0] > digilist[2]:
            return 0
        elif digilist[1] > digilist[0] and digilist[1] > digilist[2]:
            return 1
        elif digilist[2] > digilist[1] and digilist[2] > digilist[0]:
            return 2
        else:
            return -1

    def title(self):
        return f"Greatest digit: _ > _ and _"


# Card 16
# The Verifier verifies that there are more of either even
# (e.g.: 454) or odd (e.g.: 341) numbers in the code.
class MoreEvenOrOdd(Rule):
    def computation(self, value):
        digivals = digit_list(value)
        evens = list(map(lambda x: x % 2, digivals)).count(0)
        odds = list(map(lambda x: x % 2, digivals)).count(1)
        return evens < odds

    def title(self):
        return f"More even or odd?"


# Card 17
# The Verifier verifies that there is a precise number
# (that they know) of even numbers in the code:
# zero, one, two, or three.
class EvenCount(Rule):
    def computation(self, value):
        digivals = digit_list(value)
        return list(map(lambda x: x % 2, digivals)).count(0)

    def title(self):
        return f"Even count"


# Card 18
# The Verifier verifies that the sum of all the numbers in the code
# is either even or odd.
class SumParity(Rule):
    def computation(self, value):
        return sum(digit_list(value)) % 2

    def title(self):
        return "Parity of sum of digits: mod(_ + _ + _)"


# Card 19
# These cards work like cards 2 to 4, but the Verifier compares
# the sum of the and numbers to 6. This sum can be less than,
# equal to, or greater than 6.
class BlueYellowSumToSix(Rule):
    def computation(self, value):
        blue = digit_value(value, DIGIT_BLUE)
        yellow = digit_value(value, DIGIT_YELLOW)
        return comp(blue + yellow, 6)

    def title(self):
        return "Order of blue + yellow compare to 6: B + Y < = > 6"


# Card 20
# The Verifier verifies if a number repeats itself, and if it so, how many
# times. There may be no repetition (e.g.: 125), one number repeats
# itself once (e.g.: 121), or a number repeats itself twice (e.g.: 222).
# If a number repeats itself, the Verifier does not know anything about it.
# They don’t know the colour (if it’s ) or its number (a 2 or a 3, etc,).
class MaxRepetition(Rule):
    def computation(self, value):
        digits = digit_list(value)
        return max(list(map(lambda v: digits.count(v), digits)))

    def title(self):
        return "Max repetition"


# Card 21
# The Verifier verifies that there is either one pair of identical numbers
# (e.g.: 313), or no pairs of identical numbers (e.g.: 231, or 333 - which is
# not exactly a pair). If there is a pair, the Verifier does not know anything
# about it. They don’t know the colour (if it’s ) or its number (a 2 or a
# 3, etc,).
class HasPair(Rule):
    def computation(self, value):
        digits = digit_list(value)
        return max(list(map(lambda v: digits.count(v), digits))) == 2

    def title(self):
        return "Has a pair?: _XX?"


# Card 22
# The Verifier verifies that the three numbers are in either ascending
# order, descending order, or neither. For example, 223 is not ascending
# (because the three numbers do not ascend, only two).
class TotalOrder(Rule):
    def computation(self, value):
        digits = digit_list(value)
        if digits[0] < digits[1] < digits[2]:
            return -1
        elif digits[0] > digits[1] > digits[2]:
            return 1
        else:
            return 0

    def title(self):
        return "Total order: _▄█ / █▄_ / ▄_█"


# Card 23
# This card works in the same way as 19, but the Verifier compares
# the sum of all the numbers with 6.
class BlueYellowPurpleSumToSix(Rule):
    def computation(self, value):
        return comp(sum(digit_list(value)), 6)

    def title(self):
        return "Order of blue + yellow + purple compare to 6: B + Y + P < = > 6"


# Card 24
# The Verifier verifies that in the code there are consecutive increasing
# values in either a 2-digit sequence (e.g.: 312), or a 3-digit sequence
# (e.g.: 345), or none at all (e.g.: 132 - in this example the 1-3 sequence is
# increasing, but 1 and 3 are not consecutive numbers.).
class ConsecutiveIncreasingLength(Rule):
    def computation(self, value):
        digits = digit_list(value)

        if digits[2] + 1 == digits[1] and digits[1] + 1 == digits[0]:
            return 3
        elif digits[2] + 1 == digits[1] or digits[1] + 1 == digits[0]:
            return 2
        else:
            return 1

    def title(self):
        return "Consecutive increasing sequence length: 234 / _45 / ___"


# Card 25
# The Verifier verifies that there are either increasing or decreasing
# values in a 2-digit consecutive sequence (e.g.: 312 or 254), a 3-digit
# consecutive sequence (e.g.: 345 or 321), or none at all. (e.g.: 135 or
# 531 - in this example the 1-3 sequence is increasing, but 1 and 3 are not
# consecutive numbers).
# The Verifier does not know if the sequence is increasing or decreasing.
class ConsecutiveIncreasingOrDecreasingLength(Rule):
    def computation(self, value):
        digits = digit_list(value)

        if (digits[2] + 1 == digits[1] and digits[1] + 1 == digits[0]) or (
            digits[2] - 1 == digits[1] and digits[1] - 1 == digits[0]
        ):
            return 3
        elif (
            digits[2] + 1 == digits[1]
            or digits[1] + 1 == digits[0]
            or digits[2] - 1 == digits[1]
            or digits[1] - 1 == digits[0]
        ):
            return 2
        else:
            return 1

    def title(self):
        return "Consecutive (inc or dec) sequence length: 234 or 321 / _45 or 21_ / ___"


# Cards 26 to 27
# The Verifier verifies that the number of a particular colour (that they
# know) is less than 3 (e.g.: the number is less than 3).
# Watch out! If the criteria is ‘the number is less than 3’, the other
# colours’ numbers can also be less than 3... the Verifier is just not
# verifying that.
class DigitsLessThan(Rule):
    def __init__(self, value: int):
        super().__init__()
        self.value = value

    def computation(self, value):
        digits = digit_list(value)
        return [digits[2] < self.value, digits[1] < self.value, digits[0] < self.value]

    def title(self):
        return f"Digits less than {self.value}: B < {self.value} / Y < {self.value} / P < {self.value}"


# Cards 28 to 30
# The Verifier verifies that the number of a particular colour
# (that they know) is 1. (e.g.: The number is 1.)
# Watch out! The other colours’ numbers can also be 1...
# the Verifier is just not verifying that.
class DigitsEqualTo(Rule):
    def __init__(self, value: int):
        super().__init__()
        self.value = value

    def computation(self, value):
        digits = digit_list(value)
        return [
            digits[2] == self.value,
            digits[1] == self.value,
            digits[0] == self.value,
        ]

    def title(self):
        return f"Digits equal to {self.value}: B = {self.value} / Y = {self.value} / P = {self.value}"


# Cards 31 to 32
# The Verifier verifies that the number of a particular colour
# (that they know) is greater than 1.
# Watch out! The other colours’ numbers can also be greater
# than 1... the Verifier is just not verifying that.
class DigitsGreaterThan(Rule):
    def __init__(self, total: int):
        super().__init__()
        self.total = total

    def computation(self, value):
        digits = digit_list(value)
        return [digits[2] > self.total, digits[1] > self.total, digits[0] > self.total]

    def title(self):
        return f"Digits greater than {self.total}: B > {self.total} / Y > {self.total} / P > {self.total}"


# Card 33
# The Verifier verifies that the number of a particular colour
# (that they know) is odd or even. (e.g.: The number is even.)
# Watch out! The other numbers can also be even (or odd, depending).
class DigitsParity(Rule):
    def computation(self, value):
        digits = digit_list(value)
        return [digits[2] % 2, digits[1] % 2, digits[0] % 2]

    def title(self):
        return "Digits parity: B % 2 / Y % 2 / P % 2"


# Cards 34 to 35
# The Verifier verifies that the number of a particular colour is less
# than or equal to all the other numbers. (e.g.: They verify that no
# other colour is less than .)
class DigitsSmallestOrEqual(Rule):
    def computation(self, value):
        digits = digit_list(value)
        return [
            digits[2] <= digits[1] and digits[2] <= digits[0],
            digits[1] <= digits[0] and digits[1] <= digits[2],
            digits[0] <= digits[1] and digits[0] <= digits[2],
        ]

    def title(self):
        return "Digits smallest or equal: B <= Y and P / Y <= B and P / P <= Y and B"


# Cards 34 to 35
# The Verifier verifies that the number of a particular colour is less
# than or equal to all the other numbers. (e.g.: They verify that no
# other colour is less than .)
class DigitsGreatestOrEqual(Rule):
    def computation(self, value):
        digits = digit_list(value)
        return [
            digits[2] >= digits[1] and digits[2] >= digits[0],
            digits[1] >= digits[0] and digits[1] >= digits[2],
            digits[0] >= digits[1] and digits[0] >= digits[2],
        ]

    def title(self):
        return "Digits greatest or equal: B >= Y and P / Y >= B and P / P >= Y and B"


# Card 36
# The Verifier verifies that the sum of all the numbers in the code
# is a multiple of 3, or a multiple of 4, or a multiple of 5.
class SumIsMultiple(Rule):
    def computation(self, value):
        digits = digit_list(value)
        total = sum(digits)
        return [
            total % 3 == 0,
            total % 4 == 0,
            total % 5 == 0,
        ]

    def title(self):
        return "Sum is multiple of 3 / 4 / 5: B+Y+P = 3x / 4x / 5x"


# Cards 37 to 38
# The Verifier verifies that the sum of two particular numbers
# (that they know) is 4.
class TwoSum(Rule):
    def __init__(self, total: int):
        super().__init__()
        self.total = total

    def computation(self, value):
        digits = digit_list(value)
        return [
            digits[1] + digits[2] == self.total,
            digits[0] + digits[2] == self.total,
            digits[0] + digits[1] == self.total,
        ]

    def title(self):
        return f"Sum of 2 digits is {self.total}: B+Y = {self.total} / B+P = {self.total} / P+Y = {self.total}"


# Cards 39 to 41
# The Verifier verifies that the number of a particular colour (that they
# know) is less than, equal to, or greater than 1.
class DigitsCompareToValue(Rule):
    def __init__(self, midpoint: int):
        super().__init__()
        self.midpoint = midpoint

    def computation(self, value):
        digits = digit_list(value)
        return [
            comp(digits[2], self.midpoint),
            comp(digits[1], self.midpoint),
            comp(digits[0], self.midpoint),
        ]

    def title(self):
        return f"Digits compare to {self.midpoint}: B < = > {self.midpoint} / Y < = > {self.midpoint} / P < = > {self.midpoint}"


# Card 42
# The Verifier verifies that the number of a particular colour (that they
# know) is either less than or greater than either of the others (e.g.:
# The number is greater than the others).
class DigitsSmallestOrGreatest(Rule):
    def computation(self, value):
        digits = digit_list(value)
        return [
            (digits[2] < digits[1] and digits[2] < digits[0])
            or (digits[2] > digits[1] and digits[2] > digits[0]),
            (digits[1] < digits[0] and digits[1] < digits[2])
            or (digits[1] > digits[0] and digits[1] > digits[2]),
            (digits[0] < digits[1] and digits[0] < digits[2])
            or (digits[0] > digits[1] and digits[0] > digits[2]),
        ]

    def title(self):
        return "Digit is smallest/greatest: B is min or max / Y is min or max / P is min or max"


# Cards 43 to 44
# The Verifier verifies that the number is less than, equal to,
# or greater than another particular number (that they know)
class DigitCompareToOthersEither(Rule):
    def __init__(self, digit: int):
        super().__init__()
        self.digit = digit

    def computation(self, value):
        digits = digit_list(value)
        subject = digits[self.digit]
        digit1 = (self.digit + 1) % 3
        digit2 = (self.digit + 2) % 3
        v1 = digits[digit1]
        v2 = digits[digit2]
        return [
            subject < v1 or subject < v2,
            subject == v1 or subject == v2,
            subject > v1 or subject > v2,
        ]

    def title(self):
        digit1 = (self.digit + 1) % 3
        digit2 = (self.digit + 2) % 3
        return f"{digit_name(self.digit)} compare to either other colors: {digit_name(self.digit)[:1]} < {digit_name(digit1)[:1]} or {digit_name(digit2)[:1]} / {digit_name(self.digit)[:1]} = {digit_name(digit1)[:1]} or {digit_name(digit2)[:1]} / {digit_name(self.digit)[:1]} > {digit_name(digit1)[:1]} or {digit_name(digit2)[:1]}"


# Cards 45 to 47
# The Verifier verifies that the number of 1s or the number of 3s
# in the code is equal to a particular number (that they know).
class CountOfTwoNumbers(Rule):
    def __init__(self, num1: int, num2: int):
        super().__init__()
        self.num1 = num1
        self.num2 = num2

    def computation(self, value):
        digits = digit_list(value)
        return [
            digits.count(self.num1) == 0 or digits.count(self.num2) == 0,
            digits.count(self.num1) == 1 or digits.count(self.num2) == 1,
            digits.count(self.num1) == 2 or digits.count(self.num2) == 2,
        ]

    def title(self):
        return f"Count of {self.num1} OR {self.num2}: ___ or ___ / _{self.num1}_ or {self.num2}__ / {self.num1}_{self.num1} or {self.num2}{self.num2}_"


# Card 48
# The Verifier verifies that that the number of a particular colour
# (that they know) is either less than, equal to, or greater than
# that of another particular colour (that they know). (e.g.: the
# number is greater than the number.)
class TwoDigitsCompares(Rule):
    def computation(self, value):
        digits = digit_list(value)
        return [
            comp(digits[2], digits[1]),
            comp(digits[2], digits[0]),
            comp(digits[1], digits[0]),
        ]

    def title(self):
        return "Two digits compared: B < = > Y / B < = > P / Y < = > P"


RULES: list[Rule] = {
    1: LeftPointOrdering(DIGIT_BLUE),
    2: MidpointOrdering(DIGIT_BLUE, 3),
    3: MidpointOrdering(DIGIT_YELLOW, 3),
    4: MidpointOrdering(DIGIT_YELLOW, 4),
    5: EvenOdd(DIGIT_BLUE),
    6: EvenOdd(DIGIT_YELLOW),
    7: EvenOdd(DIGIT_PURPLE),
    8: NumberOrDigits(1),
    9: NumberOrDigits(3),
    10: NumberOrDigits(4),
    11: DigitOrdering(DIGIT_BLUE, DIGIT_YELLOW),
    12: DigitOrdering(DIGIT_BLUE, DIGIT_PURPLE),
    13: DigitOrdering(DIGIT_YELLOW, DIGIT_PURPLE),
    14: SmallestDigit(),
    15: GreatestDigit(),
    16: MoreEvenOrOdd(),
    17: EvenCount(),
    18: SumParity(),
    19: BlueYellowSumToSix(),
    20: MaxRepetition(),
    21: HasPair(),
    22: TotalOrder(),
    23: BlueYellowPurpleSumToSix(),
    24: ConsecutiveIncreasingLength(),
    25: ConsecutiveIncreasingOrDecreasingLength(),
    26: DigitsLessThan(3),
    27: DigitsLessThan(4),
    28: DigitsEqualTo(1),
    29: DigitsEqualTo(3),
    30: DigitsEqualTo(4),
    31: DigitsGreaterThan(1),
    32: DigitsGreaterThan(3),
    33: DigitsParity(),
    34: DigitsSmallestOrEqual(),
    35: DigitsGreatestOrEqual(),
    36: SumIsMultiple(),
    37: TwoSum(4),
    38: TwoSum(6),
    39: DigitsCompareToValue(1),
    40: DigitsCompareToValue(3),
    41: DigitsCompareToValue(4),
    42: DigitsSmallestOrGreatest(),
    43: DigitCompareToOthersEither(DIGIT_BLUE),
    44: DigitCompareToOthersEither(DIGIT_YELLOW),
    45: CountOfTwoNumbers(1, 3),
    46: CountOfTwoNumbers(3, 4),
    47: CountOfTwoNumbers(1, 4),
    48: TwoDigitsCompares(),
}
