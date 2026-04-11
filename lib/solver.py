from lib.common import *


class Solver:
    def __init__(self, secret: int):
        self.available = generate_available_numbers()
        self.secret = secret

    def draw_elimination_table(self):
        blues = set()
        yellows = set()
        purples = set()

        for i in self.available:
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
