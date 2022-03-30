"""Author: Nalongsone Danddank, Assignment #4, Feb 2 2022, ICS499 METRO STATE """

import requests
import json
from models import *
from telugu import getTeluguLogicalChars


params = {"length": 5, "attempt": 6, "language": "English", "url": "url_for('home')"}
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
    params["url"] = None
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
        words["solution"] = getTeluguLogicalChars(teluguObj.word)


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
    print("get result", words)
    solution_tlg = words["solution"]
    n = len(solution_tlg)
    if words["word_input"] == "":
        words["word_len_test"] = False
        return
    guess_tlg = getTeluguLogicalChars(words["word_input"])
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
            l = getTeluguLogicalChars(word)
            size = len(l)
            l_str = json.dumps(l)
            tlg = Telugu(word=word, length=size, list_str=l_str)
            db.session.add(tlg)
        db.session.commit()

    # for t in guess_ts:
    #     word = t.strip()
    #     l = getTeluguLogicalChars(word)
    #     size = len(l)
    #     l_str = json.dumps(l)
    #     tlg = Telugu(word=word, length=size, list_str=l_str)
    #     db.session.add(tlg)
    # db.session.commit()


def insert_word_(request, result):
    result["language"] = request.form["language"]
    result["email"] = request.form["admin_email"]
    result["pwd"] = request.form["admin_pwd"]
    result["word_insert"] = request.form["word_insert"]
    result["PASS"] = True
    print(result)
    ss = User.query.all()
    print(ss)
    # user = User(email="pink@ics499.com", pwd="pink")
    # db.session.add(user)
    # db.session.commit()


# admin@ics499.com -> ics499
def insert_word(request, db):
    result = {
        "language": request.form["language"],
        "email": request.form["admin_email"],
        "pwd": request.form["admin_pwd"],
        "word_insert": request.form["word_insert"].strip(),
        "PASS": False,
        "message": "Email Wrong!",
    }
    user = User.query.filter_by(email=result["email"]).first()
    if not user:
        return result
    if user.pwd != result["pwd"]:
        result["message"] = "Password Wrong!"
        return result

    if result["language"] == "English":
        temp = English.query.filter_by(word=result["word_insert"].lower()).first()
        if not temp:
            english = English(
                word=result["word_insert"],
                length=len(result["word_insert"]),
            )
            db.session.add(english)
            db.session.commit()
            result["word_insert"] = ""
            result["PASS"] = True
            result["message"] = "Input English Word Success!"
            return result

    elif result["language"] == "Telugu":
        temp = Telugu.query.filter_by(word=result["word_insert"]).first()
        if not temp:
            arr = getTeluguLogicalChars(result["word_insert"])
            telugu = Telugu(
                word=result["word_insert"], length=len(arr), list_str=json.dumps(arr)
            )
            db.session.add(telugu)
            db.session.commit()
            result["word_insert"] = ""
            result["PASS"] = True
            result["message"] = "Input English Word Success!"
            return result
    result["message"] = "The word already exit!"
    return result


def generate_id(request, db):
    result = {
        "language": request.form["language"],
        "email": request.form["email"],
        "pwd": request.form["pwd"],
        "word_insert": request.form["word"].strip(),
        "PASS": False,
        "message": "Email or Password Wrong!",
    }
    user = User.query.filter_by(email=result["email"]).first()
    if user and user.pwd == result["pwd"]:
        if result["language"] == "English":
            temp = CustomWord.query.filter_by(
                word=result["word_insert"].lower()
            ).first()
            print(temp)
            if not temp:
                length = len(result["word_insert"].lower())
                word = result["word_insert"].lower()
            else:
                result["message"] = "The word olready exit in your list"
                return result
        elif result["language"] == "Telugu":
            temp = CustomWord.query.filter_by(word=result["word_insert"]).first()
            if not temp:
                arr = getTeluguLogicalChars(result["word_insert"])
                length = len(arr)
                word = result["word_insert"]
            else:
                result["message"] = "The word olready exit in your list"
                return result
        cw = CustomWord(
            word=word,
            length=length,
            email=request.form["email"],
            language=result["language"],
        )
        db.session.add(cw)
        db.session.flush()
        db.session.commit()
        cw_id = cw.id
        result["word_insert"] = ""
        result["message"] = r"https://tordle.pythonanywhere.com/my_word/" + str(cw_id)
    return result


def get_word_by_id(word_id):
    cw = CustomWord.query.filter_by(id=word_id).first()
    if not cw:
        return None
    words["answer"] = cw.word
    words["solution"] = cw.word
    words["result"] = []
    words["word_input"] = ""
    words["wordCount"] = 0
    words["word_len_test"] = True
    words["status"] = "PROCESS"

    params["length"] = cw.length
    params["attempt"] = cw.length + 2
    params["language"] = cw.language
    params["url"] = word_id
    if cw.language == "Telugu":
        words["solution"] = getTeluguLogicalChars(cw.word)
    return {"words": words, "params": params}
