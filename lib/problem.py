MODES = ["Classic", "Extreme", "Nightmare"]
DIFFICULTIES = ["Easy", "Standard", "Hard"]
VERIFIERS = ["4", "5", "6"]


class Problem:
    def __init__(self, id: int, rules: list[int], secret: int, source: dict):
        self.id = id
        self.rules = rules
        self.secret = secret
        self.source = source

    def hash(self) -> str:
        return self.source["hash"]

    def mode(self) -> str:
        return MODES[int(self.source["m"])]

    def difficulty(self) -> str:
        return DIFFICULTIES[int(self.source["d"])]

    def verifiers(self) -> int:
        return self.source["n"]

    def print_header(self):
        print("═══════════════")
        print(f"Turing Machine")
        print(f"#: {self.hash()}")
        print(f"Mode: {self.mode()}")
        print(f"Difficulty: {self.difficulty()}")
        print(f"Verifiers: {self.verifiers()}")
        print("═══════════════")
