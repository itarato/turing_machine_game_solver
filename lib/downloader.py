import requests
import time
import json


class Problem:
    def __init__(self, id: int, rules: list[int], secret: int):
        self.id = id
        self.rules = rules
        self.secret = secret


def load_problems(rng: range):
    for i in rng:
        problem = load_problem(i)
        print(problem)
        time.sleep(1)


def load_problem(id: int) -> Problem:
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

    return Problem(id, parsed["ind"], parsed["code"])


if __name__ == "__main__":
    load_problems(range(1, 2))
