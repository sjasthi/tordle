"""Author: Nalongsone Danddank, Assignment #4, Feb 2 2022, ICS499 METRO STATE """

import requests
import json


l = ["0", "1", "2", "add", "font", "clone", "telugu", "english", "absolute"]
telugus = [
    "0",
    "1",
    "2",
    "సిరివె",
    "సిరివెన్నె",
    "సిరివెన్నెల",
    "సిరివెన్నెలరి",
    "సిరివెన్నెలరివె",
    "సిరివెన్నెలరివెత",
]
guess_ts = [
    "తమిళభాష",
    "సిరివెన్నెల",
    "వెన్నెలరేడు",
    "వెన్నెలకాడు",
    "సరేవీనీలా",
    "వానలసిరి",
]


def update_data(params, request, words):
    params["length"] = int(request.form["length"] or params["length"])
    params["attempt"] = int(request.form["attempt"] or params["attempt"])
    if request.form["language"] == "English":
        params["language"] = "English"
        words["solution"] = l[params["length"]]
    elif request.form["language"] == "Telugu":
        params["language"] = "Telugu"
        words["result"] = []
        words["word_input"] = ""
        words["wordCount"] = 0
        words["status"] = "PROCESS"
        words["word_len_test"] = True
        words["solution"] = getCharsFromAPI(telugus[params["length"]], "Telugu")


def getCharsFromAPI(string, language):
    """@string: String for api params
    @language: String for api params"""
    URL_char = "https://indic-wp.thisisjava.com/api/getLogicalChars.php"
    params = {"string": string, "language": language}
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
    }
    # get text or string that request from API
    r_chars = requests.get(url=URL_char, params=params, headers=headers, timeout=50)
    # handle text like json format from api by encode and decode the string.
    text = r_chars.text
    if text.startswith("\ufeff"):
        text = text.encode("utf8")[6:].decode("utf8")
    # convert text to dictionary by json
    data = json.loads(text)

    return data["data"]


STATUS = ["PROCESS", "SUCCESS", "END"]


def getResult(words):
    solution_tlg = words["solution"]
    n = len(solution_tlg)
    if words["word_input"] == "":
        words["word_len_test"] = False
        return
    guess_tlg = getCharsFromAPI(words["word_input"], "Telugu")
    if n == len(guess_tlg):
        words["word_len_test"] = True
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
        if result == [1] * n:
            words["result"].append(
                {
                    "color_arr": result,
                    "tlg_arr": guess_tlg,
                }
            )
            words["status"] = STATUS[1]
            words["wordCount"] += 1
        else:
            words["result"].append(
                {
                    "color_arr": result,
                    "tlg_arr": guess_tlg,
                }
            )
            words["status"] = STATUS[0]
            words["wordCount"] += 1
    else:
        words["word_len_test"] = False
