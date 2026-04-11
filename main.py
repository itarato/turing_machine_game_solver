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
    if len(sys.argv) != 2:
        print("Call: python3 main.py <PROBLEM-INDEX:int>")

    downloader = Downloader()

    arg1 = sys.argv[1]
    if arg1 == "custom":
        mode, difficulty, verifiers = read_custom_setting()
        problem = downloader.load_problem_by_setting(mode, difficulty, verifiers)
    else:
        problem = downloader.load_problem_by_id(arg1)

    Cli(problem).run()
