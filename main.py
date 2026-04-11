from typing import Callable
from lib.cli import *
import sys

if __name__ == "__main__":
    id = int(sys.argv[1])

    Cli().run(id)
