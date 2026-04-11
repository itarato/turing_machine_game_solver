from lib.common import *
from lib.solver import *
from lib.rules import *
from lib.downloader import *
import sys


RULES = {
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
}


class Cli:
    def __init__(self):
        pass

    def run(self, id: int):
        problem = load_problem(id)
        solver = Solver(problem.secret)
        guess = self.pick_number()
        attempt = 0

        while True:
            command = input("Command (num, rule, answer, cheat): ")

            if command == "num":
                guess = self.pick_number()
                attempt = 0
            elif command == "rule":
                attempt += 1
                rule = self.pick_rule(problem.rules)

                res = rule.analyze(solver, guess)
                if res:
                    print(color_str("It's a match", COLOR_GREEN))
                else:
                    print(color_str("It's not a match", COLOR_RED))

                draw_elimination_table(solver.available)
            elif command == "answer":
                if guess == solver.secret:
                    print(color_str(f"YES YOU WON! IT WAS {guess}", COLOR_GREEN))
                    exit()
                else:
                    print(color_str(f"NO! IT'S NOT {guess}", COLOR_RED))
            elif command == "cheat":
                self.dump_solver_state(solver)
            else:
                print(f"Unknown command `{command}`")

    def pick_rule(self, allowed_rules: list[int]) -> Rule:
        for i in allowed_rules:
            if i not in RULES:
                print(f"Rule {i} is not yet added")
                exit()

            print(color_str(f"Rule #{i}:", COLOR_BOLD) + " {RULES[i].title()}")

        i = int(input("Rule #: "))
        return RULES[i]

    def pick_number(self) -> int:
        guess = int(input("Pick a number: "))

        digilist = digit_list(guess)
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

        return guess

    def dump_solver_state(self, solver: Solver):
        print(f"Secret: {solver.secret}")
        print(f"Eliminations left: {len(solver.available)}")
        print(solver.available)
