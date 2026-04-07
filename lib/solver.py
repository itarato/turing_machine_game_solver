from lib.common import *


class Solver:
    def __init__(self, secret: int):
        self.available = generate_available_numbers()
        self.secret = secret
        self.non_immediate_rules = []
