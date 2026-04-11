from typing import Callable

import random

DIGIT_BLUE = 2
DIGIT_YELLOW = 1
DIGIT_PURPLE = 0

ORD_LT = -1
ORD_EQ = 0
ORD_GT = 1


COLOR_PURPLE = 95
COLOR_YELLOW = 93
COLOR_BLUE = 96
COLOR_RED = 91
COLOR_GREEN = 92
COLOR_GREY = 90
COLOR_DIM = 2
COLOR_BOLD = 1
COLOR_WHITE = 97


def color_str(s: str, color: int) -> str:
    return f"\x1b[{color}m{s}\x1b[0m"


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


def digit_name(d: int) -> str:
    if d == DIGIT_PURPLE:
        return "PURPLE"
    elif d == DIGIT_YELLOW:
        return "YELLOW"
    elif d == DIGIT_BLUE:
        return "BLUE"
    else:
        raise RuntimeError


def random_game_number() -> int:
    return random.randint(1, 5) * 100 + random.randint(1, 5) * 10 + random.randint(1, 5)


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


def digit_list(n: int) -> list[int]:
    return [
        digit_value(n, DIGIT_PURPLE),
        digit_value(n, DIGIT_YELLOW),
        digit_value(n, DIGIT_BLUE),
    ]


def draw_elimination_table(available: list[int]):
    blues = set()
    yellows = set()
    purples = set()

    for i in available:
        digits = digit_list(i)

        blues.add(digits[DIGIT_BLUE])
        yellows.add(digits[DIGIT_YELLOW])
        purples.add(digits[DIGIT_PURPLE])

    print(
        color_str("╔═══╗", COLOR_BLUE)
        + color_str("╔═══╗", COLOR_YELLOW)
        + color_str("╔═══╗", COLOR_PURPLE)
    )

    for i in range(1, 6):
        print(
            color_str(f"║ {i if i in blues else '-'} ║", COLOR_BLUE)
            + color_str(f"║ {i if i in yellows else '-'} ║", COLOR_YELLOW)
            + color_str(f"║ {i if i in purples else '-'} ║", COLOR_PURPLE)
        )

    print(
        color_str("╚═══╝", COLOR_BLUE)
        + color_str("╚═══╝", COLOR_YELLOW)
        + color_str("╚═══╝", COLOR_PURPLE)
    )


def print_number(n: int):
    digilist = digit_list(n)
    print(
        color_str("╔═══╗", COLOR_BLUE)
        + color_str("╔═══╗", COLOR_YELLOW)
        + color_str("╔═══╗", COLOR_PURPLE)
    )
    print(
        color_str(f"║ {digilist[DIGIT_BLUE]} ║", COLOR_BLUE)
        + color_str(f"║ {digilist[DIGIT_YELLOW]} ║", COLOR_YELLOW)
        + color_str(f"║ {digilist[DIGIT_PURPLE]} ║", COLOR_PURPLE)
    )
    print(
        color_str("╚═══╝", COLOR_BLUE)
        + color_str("╚═══╝", COLOR_YELLOW)
        + color_str("╚═══╝", COLOR_PURPLE)
    )


def print_evaluated_rules(evaluated_rules: list[list[any]]):
    for title, guess, match in evaluated_rules:
        if match:
            print(
                color_str(f"🗸 {title}", COLOR_GREEN)
                + " for "
                + color_str(str(guess), COLOR_WHITE)
            )
        else:
            print(
                color_str(f"✘ {title}", COLOR_RED)
                + " for "
                + color_str(str(guess), COLOR_WHITE)
            )


def clear_screen():
    print("\033[2J\033[H", end="")
