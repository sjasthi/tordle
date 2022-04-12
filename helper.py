"""Author: Nalongsone Danddank, Assignment #4, Feb 2 2022, ICS499 METRO STATE """

import requests
import json
from models import *
from telugu import getTeluguLogicalChars, isTeluguWord, isEnglish
from flask import flash


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
            result["message"] = "Input Telugu Word Success!"
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
                result["message"] = (
                    "The word already input by :\n\t\t"
                    + temp.email
                    + "\nThe exit link is: \n\t\t"
                    + "https://tordle.pythonanywhere.com/my_word/"
                    + str(temp.id)
                )
                return result
        elif result["language"] == "Telugu":
            temp = CustomWord.query.filter_by(word=result["word_insert"]).first()
            if not temp:
                arr = getTeluguLogicalChars(result["word_insert"])
                length = len(arr)
                word = result["word_insert"]
            else:
                result["message"] = (
                    "The word already input by :\n\t\t"
                    + temp.email
                    + "\nThe exit link is: \n\t\t"
                    + "https://tordle.pythonanywhere.com/my_word/"
                    + str(temp.id)
                )
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


result = {
    "language": "English",
    "length": "all",
    "num_page": 15,
    "word_list": None,
}


def get_system_list(request):
    page = request.args.get("page", 1, type=int)
    english_list = English.query.order_by(English.length).paginate(
        page=page, per_page=15
    )
    result["word_list"] = english_list
    result["num_page"] = 15
    if request.form:
        result["language"] = request.form["language"]
        result["length"] = request.form["length"]
        result["key_word"] = request.form["key_word"]
    else:
        result["language"] = "English"
        result["length"] = "all"
        result["key_word"] = ""
    return result


def get_system_list_search(request):
    length = "all"
    language = "English"
    num_page = 15
    page = 1
    key_word = ""
    if request.args:
        language = request.args.get("language", "English", type=str)
        num_page = int(request.args.get("num_page", 15, type=int))
        page = request.args.get("page", 1, type=int)
        length = request.args.get("length", "all", type=int)
        key_word = request.args.get("key_word", "", type=str)
    result = get_system_list(request)
    if request.form:
        num_page = 15
        length = request.form["length"]
        language = request.form["language"]
        key_word = request.form["key_word"]
    word_list = None
    if length == "all":
        if language == "English":
            word_list = (
                English.query.filter(English.word.like(f"%{key_word}%"))
                .order_by(English.length)
                .paginate(page=page, per_page=num_page)
            )
        elif language == "Telugu":
            word_list = (
                Telugu.query.filter(Telugu.word.like(f"%{key_word}%"))
                .order_by(Telugu.length)
                .paginate(page=page, per_page=num_page)
            )
    else:
        length = int(length)
        if language == "English":
            word_list = (
                English.query.filter(English.word.like(f"%{key_word}%"))
                .filter(English.length == length)
                .paginate(page=page, per_page=num_page)
            )
        elif language == "Telugu":
            word_list = (
                Telugu.query.filter(Telugu.word.like(f"%{key_word}%"))
                .filter(Telugu.length == length)
                .paginate(page=page, per_page=num_page)
            )

    result["word_list"] = word_list
    result["language"] = language
    result["length"] = length
    result["key_word"] = key_word
    return result


def handle_delete_word(word, request):
    if result["language"] == "English":
        english = English.query.get_or_404(word)
        db.session.delete(english)
        db.session.commit()
        flash("Your word has been deleted from system!", "success")
    elif result["language"] == "Telugu":
        telugu = Telugu.query.get_or_404(word)
        db.session.delete(telugu)
        db.session.commit()
        flash("Your post has been deleted from system!", "success")


def handle_edit_word(request):
    if (
        request.form["new_word"] != ""
        and request.form["new_word"] != request.form["old_word"]
    ):
        if request.form["language"] == "English":
            new_english = English.query.filter_by(word=request.form["new_word"]).first()
            if not new_english:
                old_english = English.query.filter_by(
                    word=request.form["old_word"]
                ).first()
                old_english.word = request.form["new_word"]
                old_english.length = len(request.form["new_word"])
                db.session.commit()
                flash("Your word has been Updated for system!", "success")
            else:
                flash("You cannot update dupicate words for system!", "danger")

        elif request.form["language"] == "Telugu":
            new_telugu = Telugu.query.filter_by(word=request.form["new_word"]).first()
            if not new_telugu:
                old_telugu = Telugu.query.filter_by(
                    word=request.form["old_word"]
                ).first()
                old_telugu.word = request.form["new_word"]
                arr = getTeluguLogicalChars(request.form["new_word"])
                old_telugu.length = len(arr)
                db.session.commit()
                flash("Your word has been Updated for system!", "success")
            else:
                flash("You cannot update dupicate words for system!", "danger")
    else:
        flash("You have done nothing for system!", "danger")


def get_custom_list(request):
    length = "all"
    language = "all"
    num_page = 15
    page = 1
    email = ""
    key_word = ""
    words = CustomWord.query.order_by(CustomWord.length).paginate(
        page=page, per_page=num_page
    )
    result = {
        "language": language,
        "length": length,
        "word_list": words,
        "email": email,
        "key_word": key_word,
    }
    if request.args:
        language = request.args.get("language", "English", type=str)
        num_page = int(request.args.get("num_page", 15, type=int))
        page = request.args.get("page", 1, type=int)
        length = request.args.get("length", "all", type=int)
        key_word = request.args.get("key_word", "", type=str)
        email = request.args.get("email", "", type=str)
    if request.form:
        num_page = 15
        length = request.form["length"]
        language = request.form["language"]
        key_word = request.form["key_word"]
        email = request.form["email"]

    if length == "all":
        if language == "all":
            words = (
                CustomWord.query.filter(CustomWord.word.like(f"%{key_word}%"))
                .filter(CustomWord.email.like(f"%{email}%"))
                .order_by(CustomWord.length)
                .paginate(page=page, per_page=num_page)
            )
        else:
            words = (
                CustomWord.query.filter_by(language=language)
                .filter(CustomWord.email.like(f"%{email}%"))
                .filter(CustomWord.word.like(f"%{key_word}%"))
                .order_by(CustomWord.id)
                .paginate(page=page, per_page=num_page)
            )
    else:
        length = int(length)
        if language == "all":
            words = (
                CustomWord.query.filter_by(length=length)
                .filter(CustomWord.email.like(f"%{email}%"))
                .filter(CustomWord.word.like(f"%{key_word}%"))
                .order_by(CustomWord.id)
                .paginate(page=page, per_page=num_page)
            )
        else:
            words = (
                CustomWord.query.filter_by(length=length)
                .filter_by(language=language)
                .filter(CustomWord.email.like(f"%{email}%"))
                .filter(CustomWord.word.like(f"%{key_word}%"))
                .order_by(CustomWord.id)
                .paginate(page=page, per_page=num_page)
            )

    result["word_list"] = words
    result["language"] = language
    result["length"] = length
    result["key_word"] = key_word
    result["email"] = email
    return result


def handle_delete_custom_word(request, word_id):
    custom_word = CustomWord.query.get_or_404(word_id)
    db.session.delete(custom_word)
    db.session.commit()
    flash("Your word has been deleted from List!", "success")


def handle_edit_custom_word(request):
    print(request.form)
    id = int(request.form["word_id"])
    word = CustomWord.query.get_or_404(id)
    if word.word != (request.form["word"]).strip():
        word.word = (request.form["word"]).strip()
        if isEnglish((request.form["word"]).strip()):
            word.length = len((request.form["word"]).strip())
        elif isTeluguWord((request.form["word"]).strip()):
            arr = getTeluguLogicalChars((request.form["word"]).strip())
            word.length = len(arr)
    if word.language != request.form["language"]:
        word.language = request.form["language"]
    if word.email != (request.form["email"]).strip():
        word.email = (request.form["email"]).strip()
    db.session.commit()
    flash("Your word has been Updated from List!", "success")
