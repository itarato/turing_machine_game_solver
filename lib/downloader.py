import requests
import time
import json
import pickle
import sys
from lib.common import *
from lib.problem import *

CACHE_FILE_PATH = "./cache/problems.pkl"
UUID = "6d4918c2-ab2b-408d-a186-6308deb6f144"
HEADERS = {
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


class Downloader:
    def __init__(self):
        try:
            self.cache = pickle.load(open(CACHE_FILE_PATH, "rb"))
        except:
            self.cache = {}

    def load_problems(self, rng: range):
        for i in rng:
            problem = self.load_problem_by_id(i)
            print(problem.source)

    def load_problem_by_id(self, id: str) -> Problem:
        if id in self.cache:
            parsed = self.cache[id]
        else:
            parsed = self.load_source_by_id(id)
            time.sleep(1)

        try:
            return Problem(id, parsed["ind"], parsed["code"], parsed)
        except Exception as e:
            print(f"Error at parsing downloaded problem #{id}: {parsed} Error: {e}")
            exit()

    def load_problem_by_setting(
        self, mode: int, difficulty: int, verifiers: int
    ) -> Problem:
        parsed = self.load_source_by_setting(mode, difficulty, verifiers)
        try:
            return Problem(id, parsed["ind"], parsed["code"], parsed)
        except Exception as e:
            print(f"Error at parsing downloaded problem #{id}: {parsed} Error: {e}")
            exit()

    def load_todays_problem(self) -> Problem:
        ts = int(time.time())
        parsed = self.load_source_for_timestamp(ts)

        try:
            return Problem(id, parsed["ind"], parsed["code"], parsed)
        except Exception as e:
            print(f"Error at parsing downloaded problem #{id}: {parsed} Error: {e}")
            exit()

    def load_source_by_id(self, id: str) -> dict:
        url = "https://turingmachine.info/api/api.php"
        params = {"uuid": UUID, "h": id}
        response = requests.get(url, params=params, headers=HEADERS)

        assert response.status_code == 200
        parsed = json.loads(response.text)

        self.cache[id] = parsed
        pickle.dump(self.cache, open(CACHE_FILE_PATH, "wb"))

        return parsed

    def load_source_for_timestamp(self, ts: int) -> dict:
        url = "https://turingmachine.info/api/api.php"
        params = {"uuid": UUID, "s": "1", "curDate": str(ts)}
        response = requests.get(url, params=params, headers=HEADERS)

        assert response.status_code == 200
        parsed = json.loads(response.text)

        self.cache[parsed["hash"]] = parsed
        pickle.dump(self.cache, open(CACHE_FILE_PATH, "wb"))

        return parsed

    # Mode: 0-2
    # Difficulty: 0-2
    # Verifiers: 4-6
    def load_source_by_setting(
        self, mode: int, difficulty: int, verifiers: int
    ) -> dict:
        url = "https://turingmachine.info/api/api.php"
        params = {
            "uuid": UUID,
            "m": str(mode),
            "d": str(difficulty),
            "n": str(verifiers),
        }
        response = requests.get(url, params=params, headers=HEADERS)

        assert response.status_code == 200
        parsed = json.loads(response.text)

        self.cache[parsed["hash"]] = parsed
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
