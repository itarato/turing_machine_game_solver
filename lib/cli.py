from lib.common import *
from lib.solver import *
from lib.rules import *
from lib.downloader import *
from simple_term_menu import TerminalMenu

CMD_NUM = "Pick a new number"
CMD_RULE = "Evaluate a rule card"
CMD_CHEAT = "Cheat"
CMD_ANSWER = "Answer"
CMD_EXIT = "Exit"

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
        clear_screen()

        problem = load_problem(id)
        solver = Solver(problem.secret)
        guess = self.pick_number()
        attempt = 0
        evaluated_rules = []

        while True:
            commands = [CMD_RULE, CMD_NUM, CMD_ANSWER, CMD_CHEAT, CMD_EXIT]
            menu = TerminalMenu(commands)
            command = commands[menu.show()]

            if command == CMD_NUM:
                guess = self.pick_number()
                attempt = 0
            elif command == CMD_RULE:
                if attempt >= 3:
                    print("Need to pick a new number")
                    continue

                attempt += 1
                rule = self.pick_rule(problem.rules)
                res = rule.analyze(solver, guess)

                if res:
                    print(color_str("It's a match", COLOR_GREEN))
                else:
                    print(color_str("It's not a match", COLOR_RED))

                evaluated_rules.append([rule.title(), guess, res])
            elif command == CMD_ANSWER:
                if guess == solver.secret:
                    print(color_str(f"YES YOU WON! IT WAS {guess}", COLOR_GREEN))
                    exit()
                else:
                    print(color_str(f"NO! IT'S NOT {guess}", COLOR_RED))
                continue
            elif command == CMD_CHEAT:
                self.dump_solver_state(solver)
                continue
            elif command == CMD_EXIT:
                exit()
            else:
                raise RuntimeError

            clear_screen()
            print_number(guess)
            draw_elimination_table(solver.available)
            print_evaluated_rules(evaluated_rules)

    def pick_rule(self, allowed_rules: list[int]) -> Rule:
        options = []
        for i in allowed_rules:
            if i not in RULES:
                print(f"Rule {i} is not yet added")
                exit()

            options.append(RULES[i].title())

        menu = TerminalMenu(options)
        selected = menu.show()

        return RULES[allowed_rules[selected]]

    def pick_number(self) -> int:
        allowed = list(range(1, 6))
        while True:
            n = int(input("Pick a number: "))
            if n < 111 or n > 555:
                print("Invalid number. Must be 111-555 only 1-5s")
                continue

            digits = digit_list(n)
            if (
                digits[0] not in allowed
                or digits[1] not in allowed
                or digits[2] not in allowed
            ):
                print("Invalid number. Must be 111-555 only 1-5s")
                continue

            return n

    def dump_solver_state(self, solver: Solver):
        print(f"Secret: {solver.secret}")
        print(f"Eliminations left: {len(solver.available)}")
        print(solver.available)
