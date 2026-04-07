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


def eliminate(available: list[int], fn: Callable[[int], bool]):
    for i in range(len(available) - 1, -1, -1):
        if fn(available[i]):
            available.pop(i)
