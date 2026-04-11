import requests
import time
import json
import pickle
import sys

CACHE_FILE_PATH = "./cache/problems.pkl"


class Problem:
    def __init__(self, id: int, rules: list[int], secret: int):
        self.id = id
        self.rules = rules
        self.secret = secret


class Downloader:
    def __init__(self):
        try:
            self.cache = pickle.load(open(CACHE_FILE_PATH, "rb"))
        except:
            self.cache = {}

    def load_problems(self, rng: range):
        for i in rng:
            problem = self.load_problem(i)
            print(problem)

    def load_problem(self, id: int) -> Problem:
        if id in self.cache:
            parsed = self.cache[id]
        else:
            parsed = self.load_source(id)
            time.sleep(1)

        return Problem(id, parsed["ind"], parsed["code"])

    def load_source(self, id: int) -> dict:
        url = "https://turingmachine.info/api/api.php"
        params = {"uuid": "6d4918c2-ab2b-408d-a186-6308deb6f144", "h": str(id)}
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:149.0) Gecko/20100101 Firefox/149.0",
            "Accept": "*/*",
            "Accept-Language": "en-CA,en-US;q=0.9,en;q=0.8",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Referer": "https://www.turingmachine.info/",
            "Origin": "https://www.turingmachine.info",
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "Priority": "u=4",
        }

        response = requests.get(url, params=params, headers=headers)

        assert response.status_code == 200
        parsed = json.loads(response.text)

        self.cache[id] = parsed
        pickle.dump(self.cache, open(CACHE_FILE_PATH, "wb"))

        return parsed


if __name__ == "__main__":
    if len(sys.argv) == 3:
        start = int(sys.argv[1])
        end = int(sys.argv[2])
    else:
        start = 1
        end = 1

    dl = Downloader()
    dl.load_problems(range(start, end + 1))
