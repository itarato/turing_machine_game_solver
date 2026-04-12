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
CMD_TOGGLE_ELIMINATOR = "Toggle elimination chart"


class EvaluatedRule:
    def __init__(self, rule: Rule, guess: int, match: bool):
        self.rule = rule
        self.guess = guess
        self.match = match


class Cli:
    def __init__(self, problem: Problem):
        self.problem = problem
        self.solver = Solver(self.problem.secret)
        self.evaluated_rules: list[EvaluatedRule] = []
        self.guess: None | int = None
        self.eliminator_on: bool = True
        self.attempt: int = 0

    def run(self):
        while True:
            if self.guess is None:
                self.refresh_screen()
                command = CMD_NUM
            else:
                commands = [
                    CMD_NUM,
                    CMD_ANSWER,
                    CMD_TOGGLE_ELIMINATOR,
                    CMD_CHEAT,
                    CMD_EXIT,
                ]
                if attempt < 3:
                    commands.insert(0, CMD_RULE)

                menu = TerminalMenu(commands)
                cmd_index = menu.show()
                if cmd_index is None:
                    command = CMD_EXIT
                else:
                    command = commands[cmd_index]

            if command == CMD_NUM:
                self.guess = self.pick_number()
                attempt = 0
            elif command == CMD_RULE:
                attempt += 1
                rule = self.pick_rule(self.problem.rules)
                if rule is None:
                    continue

                res = rule.analyze(self.solver, self.guess)

                if res:
                    print(color_str("It's a match", COLOR_GREEN))
                else:
                    print(color_str("It's not a match", COLOR_RED))

                self.evaluated_rules.append(EvaluatedRule(rule, self.guess, res))
            elif command == CMD_ANSWER:
                answer = self.pick_number("Your guess is: ")
                if answer == self.solver.secret:
                    print(color_str(f"YES YOU WON! IT WAS {answer}", COLOR_GREEN))
                    exit()
                else:
                    print(color_str(f"NO! IT'S NOT {answer}", COLOR_RED))
                continue
            elif command == CMD_CHEAT:
                self.dump_solver_state(self.solver)
                continue
            elif command == CMD_TOGGLE_ELIMINATOR:
                self.eliminator_on = not self.eliminator_on
            elif command == CMD_EXIT:
                exit()
            else:
                raise RuntimeError

            self.refresh_screen()

    def pick_rule(self, allowed_rules: list[int]) -> None | Rule:
        options = []
        for i in allowed_rules:
            if i not in RULES:
                print(f"Rule {i} is not yet added")
                exit()

            options.append(RULES[i].title())

        menu = TerminalMenu(options)
        selected = menu.show()
        if selected is None:
            return None

        return RULES[allowed_rules[selected]]

    def pick_number(self, prompt: str = "Pick a number: ") -> int:
        allowed = list(range(1, 6))
        while True:
            try:
                n = int(input(prompt))
            except:
                print("Invalid number. Must be 111-555 only 1-5s")
                continue
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

    def print_evaluated_rules(self):
        for evaluated_rule in self.evaluated_rules:
            if evaluated_rule.match:
                print(
                    color_str(f"🗸 {evaluated_rule.rule.title()}", COLOR_GREEN)
                    + " for "
                    # + color_str(str(evaluated_rule.guess), COLOR_WHITE)
                    + colorize_digits(evaluated_rule.guess)
                )
            else:
                print(
                    color_str(f"✘ {evaluated_rule.rule.title()}", COLOR_RED)
                    + " for "
                    # + color_str(str(evaluated_rule.guess), COLOR_WHITE)
                    + colorize_digits(evaluated_rule.guess)
                )

    def print_number(self):
        if self.guess is None:
            digilist = ["?", "?", "?"]
        else:
            digilist = digit_list(self.guess)

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

    def refresh_screen(self):
        clear_screen()
        self.problem.print_header()
        self.print_number()
        if self.eliminator_on:
            self.solver.draw_elimination_table()
        self.print_evaluated_rules()
