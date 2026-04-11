from lib.cli import *
import sys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Call: python3 main.py <PROBLEM-INDEX:int>")

    id = int(sys.argv[1])
    Cli().run(id)
