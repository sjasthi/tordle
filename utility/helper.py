"""Author: Nalongsone Danddank, Assignment #4, Feb 2 2022, ICS499 METRO STATE """

import requests
import json


def update_data(params, request, words):
    params["length"] = int(request.form["length"] or params["length"])
    params["attempt"] = int(request.form["attempt"] or params["attempt"])
    params["language"] = (request.form["language"]) or params["language"]
    words["guess"] = request.form.get("word") or words["guess"]


def getCharsFromAPI(string, language):
    """@string: String for api params
    @language: String for api params"""
    URL_char = "https://indic-wp.thisisjava.com/api/getLogicalChars.php"
    params = {"string": string, "language": language}
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
    }
    # get text or string that request from API
    r_chars = requests.get(url=URL_char, params=params, headers=headers, timeout=5)
    # handle text like json format from api by encode and decode the string.
    text = r_chars.text
    if text.startswith("\ufeff"):
        text = text.encode("utf8")[6:].decode("utf8")
    # convert text to dictionary by json
    data = json.loads(text)

    return data["data"]


def getResult(solution_tlg, guess):
    n = len(solution_tlg)
    guess_tlg = getCharsFromAPI(guess, "Telugu")
    if n == len(guess_tlg):
        solution_base = [x[0] for x in solution_tlg]
        guess_base = [x[0] for x in guess_tlg]
        result = [0] * n
        for i in range(n):
            if guess_tlg[i] == solution_tlg[i]:
                result[i] = 1
            else:
                for j in range(n):
                    if guess_tlg[i] == solution_tlg[j]:
                        result[i] = 2
                        break
        for i in range(n):
            if (solution_base[i] == guess_base[i]) and (result[i] not in [1, 2]):
                result[i] = 3
            else:
                for j in range(n):
                    if (guess_base[i] == solution_base[j]) and (
                        result[i] not in [1, 2, 3]
                    ):
                        result[i] = 4
                        break
        return [guess_tlg, result]
    return []
