from __future__ import annotations
from typing import Callable

DIGIT_BLUE = 2
DIGIT_YELLOW = 1
DIGIT_PURPLE = 0

ORD_LT = -1
ORD_EQ = 0
ORD_GT = 1


def generate_available_numbers(digit: int = DIGIT_BLUE) -> list[int]:
    if digit == DIGIT_PURPLE:
        return list(range(1, 6))
    else:
        return sum(
            [
                list(
                    map(
                        lambda j: i * (10**digit) + j,
                        generate_available_numbers(digit - 1),
                    )
                )
                for i in range(1, 6)
            ],
            [],
        )


def digit_value(number, digit) -> int:
    return (number // (10**digit)) % 10


def comp(lhs: int, rhs: int) -> int:
    if lhs < rhs:
        return ORD_LT
    elif lhs == rhs:
        return ORD_EQ
    elif lhs > rhs:
        return ORD_GT
    else:
        raise RuntimeError


class Solver:
    def __init__(self, secret: int):
        self.available = generate_available_numbers()
        self.secret = secret
        self.non_immediate_rules = []

    def guess(self, guess: int, rule: Rule):
        rule.analyze(self, guess)


class Rule:
    def __init__(self):
        self.exhausted = False

    def analyze(self, secret: int, guess: int):
        raise NotImplementedError


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
        self.eliminate(solver.available, eliminator_fn)

        self.exhausted = True

    def eliminate(self, available: list[int], fn: Callable[[int], bool]):
        for i in range(len(available) - 1, -1, -1):
            if fn(available[i]):
                available.pop(i)

    def make_eliminator_fn(
        self,
        guess_ord: int,
        ord_match: bool,  # Eg.: False
    ) -> Callable[[int], bool]:
        midpoint = self.midpoint
        digit = self.digit
        return (
            lambda n: (comp(digit_value(n, digit), midpoint) == guess_ord) ^ ord_match
        )


if __name__ == "__main__":
    solver = Solver(341)
    solver.guess(332, MidpointOrdering(DIGIT_BLUE, 3))
    print(solver.available)
