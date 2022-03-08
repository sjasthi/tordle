"""Author: Nalongsone Danddank, Assignment #4, Feb 2 2022, ICS499 METRO STATE """

import requests
import json
from models import *


params = {"length": 5, "attempt": 6, "language": "English"}
english_random = getRandomWordByLength(params["length"], "English")
words = {
    "answer": english_random,
    "solution": english_random,
    "result": [],
    "word_input": "",
    "wordCount": 0,
    "word_len_test": True,
    "status": "PROCESS",
}


def update_data(params, request, words):
    params["length"] = int(request.form["length"] or params["length"])
    params["attempt"] = int(request.form["attempt"] or params["attempt"])
    if request.form["language"] == "English":
        params["language"] = "English"
        english_random = getRandomWordByLength(params["length"], "English")
        words["answer"] = english_random
        words["solution"] = english_random
    elif request.form["language"] == "Telugu":
        params["language"] = "Telugu"
        words["result"] = []
        words["word_input"] = ""
        words["wordCount"] = 0
        words["status"] = "PROCESS"
        words["word_len_test"] = True
        teluguObj = getRandomWordByLength(params["length"], "Telugu")
        words["answer"] = teluguObj.word
        words["solution"] = json.loads(teluguObj.list_str)


def getCharsFromAPI(string, language):
    """@string: String for api params
    @language: String for api params"""
    URL_char = "https://indic-wp.thisisjava.com/api/getLogicalChars.php"
    # URL_char = "http://localhost/indic-wp//api/getLogicalChars.php"
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


def englishFile2db(file, db, English):
    # db.drop_all()
    # db.create_all()
    with open(file, "r") as f:
        for line in f:
            word = line.strip().lower()
            size = len(word)
            if size >= 3:
                eng = English(word=word, length=size)
                db.session.add(eng)
        db.session.commit()


def teluguFile2db(file, db, Telugu):
    # db.drop_all()
    # db.create_all()
    with open(file, "r") as f:
        for line in f:
            word = line.strip()
            l = getCharsFromAPI(word, "Telugu")
            size = len(l)
            l_str = json.dumps(l)
            tlg = Telugu(word=word, length=size, list_str=l_str)
            db.session.add(tlg)
        db.session.commit()

    # for t in guess_ts:
    #     word = t.strip()
    #     l = getCharsFromAPI(word, "Telugu")
    #     size = len(l)
    #     l_str = json.dumps(l)
    #     tlg = Telugu(word=word, length=size, list_str=l_str)
    #     db.session.add(tlg)
    # db.session.commit()
