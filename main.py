from lib.cli import *
from lib.downloader import *
from simple_term_menu import TerminalMenu
import sys


def read_custom_setting() -> tuple[int, int, int]:
    print("Mode:")
    mi = TerminalMenu(MODES).show()

    print("Difficulty:")
    di = TerminalMenu(DIFFICULTIES).show()

    print("Verifiers:")
    verifiers = TerminalMenu(VERIFIERS).show()

    return (mi, di, verifiers + 4)


if __name__ == "__main__":
    downloader = Downloader()

    print("Load challenge:")
    options = ["Custom", "Daily", "By ID"]
    i = TerminalMenu(options).show()
    if i is None:
        exit()

    if i == 0:
        mode, difficulty, verifiers = read_custom_setting()
        problem = downloader.load_problem_by_setting(mode, difficulty, verifiers)
    elif i == 1:
        problem = downloader.load_todays_problem()
    elif i == 2:
        id = input("ID: ")
        problem = downloader.load_problem_by_id(id)

    Cli(problem).run()
