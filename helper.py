"""Author: Nalongsone Danddank, Final Project, begin on Feb 2 2022, ICS499 METRO STATE """


from forms import *

params = {
    "length": 5,
    "attempt": 6,
    "language": "English",
    "url": "url_for('home')",
    "statics": {"numAttempts": 0, "percentWin": 0, "WinStreak": 0, "bestStreak": 0},
}


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def getRandomWordByLength(length, language):
    if language == "English":
        results = (
            English.query.filter_by(length=length)
            .filter(func.DATE(English.latest_play_time).isnot(date.today()))
            .all()
        )
        if not results:
            return "#####"
        result = random.choice(results)
        english = English.query.filter_by(word=result.word).first()
        english.latest_play_time = datetime.now()
        db.session.commit()
        return result.word
    elif language == "Telugu":

        results = (
            Telugu.query.filter_by(length=length)
            .filter(func.DATE(Telugu.latest_play_time).isnot(date.today()))
            .all()
        )
        if not results:
            return "#####"
        result = random.choice(results)
        telugu = Telugu.query.filter_by(word=result.word).first()
        telugu.latest_play_time = datetime.now()
        db.session.commit()
        return result


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


def getParams():
    return {
        "length": 5,
        "attempt": 6,
        "language": "English",
        "url": "url_for('home')",
        "statics": {"numAttempts": 0, "percentWin": 0, "WinStreak": 0, "bestStreak": 0},
    }


def getStatics(current_user, sendJson, db, params):
    if sendJson:
        record = Record(
            user_id=current_user.id,
            word=sendJson["answer"],
            is_win=sendJson["is_win"],
            state="streak",
        )
        db.session.add(record)
        db.session.commit()
        print("Record: " + str(record))
    records = Record.query.filter_by(user_id=current_user.id).order_by(Record.id).all()
    if not records:
        return None
    # Number of Attempts:
    params["statics"]["numAttempts"] = len(records)
    # Percent Wins
    params["statics"]["percentWin"] = (
        str(
            100
            * (1.0 * sum(map(lambda x: 1 if x.is_win else 0, records)) / len(records))
        )
        + "%"
    )
    # # Winning StreakL
    records_ = list(records)
    current_streak = list(map(lambda x: 1 if x.is_win else 0, records_))
    if current_streak[-1] == 0:
        params["statics"]["WinStreak"] = 0
    else:
        winStreak_count = 0
        while current_streak and current_streak[-1] != 0:
            current_streak.pop()
            winStreak_count += 1
        params["statics"]["WinStreak"] = winStreak_count
    # Best strak:
    record_str = "".join(map(lambda x: "1" if x.is_win else "0", records))
    ans_list = record_str.split("0")
    max_len = 0
    for s in ans_list:
        if max_len < len(s):
            max_len = len(s)
    params["statics"]["bestStreak"] = max_len
    print("update statics params: ")
    print(params)
    return params


def refess_data(params, request, words):
    print(request.form)
    params["length"] = int(request.form["length"] or params["length"])
    params["attempt"] = int(request.form["attempt"] or params["attempt"])
    params["url"] = None
    if request.form["language"] == "English":
        params["language"] = "English"
        english_random = getRandomWordByLength(params["length"], "English")
        # words["answer"] = english_random
        # words["solution"] = english_random
    elif request.form["language"] == "Telugu":
        params["language"] = "Telugu"
        # words["result"] = []
        # words["word_input"] = ""
        # words["wordCount"] = 0
        # words["status"] = "PROCESS"
        # words["word_len_test"] = True
        # teluguObj = getRandomWordByLength(params["length"], "Telugu")
        # if teluguObj != "#####":
        #     words["answer"] = teluguObj.word
        #     words["solution"] = getTeluguLogicalChars(teluguObj.word)
        # else:
        #     words["answer"] = "#####"
        #     words["solution"] = []


def update_data(params, request, words):
    print(request.form)
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
        if teluguObj != "#####":
            words["answer"] = teluguObj.word
            words["solution"] = getTeluguLogicalChars(teluguObj.word)
        else:
            words["answer"] = "#####"
            words["solution"] = []


# def getCharsFromAPI(string, language):
#     """@string: String for api params
#     @language: String for api params"""
#     URL_char = "https://indic-wp.thisisjava.com/api/getLogicalChars.php"
#     # URL_char = "http://localhost/indic-wp//api/getLogicalChars.php"
#     params = {"string": string, "language": language}
#     headers = {
#         "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
#     }
#     # get text or string that request from API
#     r_chars = requests.get(url=URL_char, params=params, headers=headers, timeout=50)
#     # handle text like json format from api by encode and decode the string.
#     text = r_chars.text
#     if text.startswith("\ufeff"):
#         text = text.encode("utf8")[6:].decode("utf8")
#     # convert text to dictionary by json
#     data = json.loads(text)

#     return data["data"]


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


# admin@ics499.com -> ics499
def insert_word(request, db):
    result = {
        "language": request.form["language"],
        "word_insert": request.form["word_insert"].strip(),
        "PASS": False,
        "message": "Email Wrong!",
    }

    if result["language"] == "English":
        word_insert = result["word_insert"].strip().lower()
        if not isEnglish(word_insert):
            flash("You have input correct English word!", "danger")
            return result
        temp = English.query.filter_by(word=word_insert).first()
        if not temp:
            english = English(
                word=word_insert,
                length=len(word_insert),
            )
            db.session.add(english)
            db.session.commit()
            result["word_insert"] = ""
            result["PASS"] = True
            result["message"] = "Input English Word Success!"
            return result

    elif result["language"] == "Telugu":
        word_insert = result["word_insert"].strip()
        if not isTeluguWord(word_insert):
            flash("You have input correct Telugu word!", "danger")
            return result
        temp = Telugu.query.filter_by(word=word_insert).first()
        if not temp:
            arr = getTeluguLogicalChars(word_insert)
            telugu = Telugu(word=word_insert, length=len(arr))
            db.session.add(telugu)
            db.session.commit()
            result["word_insert"] = ""
            result["PASS"] = True
            result["message"] = "Input Telugu Word Success!"
            return result
    result["message"] = "The word already exit in the System!"
    return result


def generate_id(request, db, current_user):
    result = {
        "language": request.form["language"],
        "word_insert": request.form["word"].strip(),
        "PASS": False,
        "message": "Email or Password Wrong!",
    }
    print(result)
    word = None
    if result["language"] == "English":
        word_insert = (result["word_insert"]).lower()
        if not isEnglish(word_insert):
            flash("You have input correct English word!", "danger")
            result["message"] = "You have input correct English word!"
            return result
        temp = CustomWord.query.filter_by(word=word_insert).first()
        if not temp:
            length = len(word_insert)
            word = word_insert
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
        word_insert = result["word_insert"].strip()
        if not isTeluguWord(word_insert):
            flash("You have input correct Telugu word!", "danger")
            result["message"] = "You have input correct Telugu word!"
            return result
        temp = CustomWord.query.filter_by(word=word_insert).first()
        if not temp:
            arr = getTeluguLogicalChars(word_insert)
            length = len(arr)
            word = word_insert
        else:
            result["message"] = (
                "The word already input by :\n\t\t"
                + temp.email
                + "\nThe exit link is: \n\t\t"
                + "https://tordle.pythonanywhere.com/my_word/"
                + str(temp.id)
            )
            return result
    if word:
        print(word)
        cw = CustomWord(
            word=word,
            length=length,
            email=current_user.email,
            language=result["language"],
            user_id=current_user.id,
            create_time=datetime.utcnow(),
        )
        db.session.add(cw)
        # db.session.flush()
        db.session.commit()
        result["word_insert"] = ""
        result["message"] = r"https://tordle.pythonanywhere.com/my_word/" + str(cw.id)
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
    db.session.commit()
    flash("Your word has been Updated from List!", "success")


def get_user_list(request):
    page = request.args.get("page", 1, type=int)
    users = User.query.order_by(User.id).paginate(page=page, per_page=15)
    result["users"] = users
    return result


def handle_edit_user(request):
    id = int(request.form["user_id"])
    user = User.query.get_or_404(id)
    user.email = request.form["email"].strip()
    user.password = request.form["password"].strip()
    user.role = request.form["role"]
    db.session.commit()
    flash("Your word has been Updated from List!", "success")


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
            tlg = Telugu(word=word, length=size)
            db.session.add(tlg)
        db.session.commit()


def initUser(db, User):
    user_admin = User(
        email="admin@ics499.com",
        password="ics499",
        role="admin",
    )
    db.session.add(user_admin)
    user1 = User(
        email="ping@ics499.com",
        password="ics499",
        role="member",
    )
    db.session.add(user1)
    user2 = User(
        email="ics499@gmail.com",
        password="spring22",
        role="member",
    )
    db.session.add(user2)
    user3 = User(
        email="ics325@gmail.com",
        password="summer21",
        role="member",
    )
    db.session.add(user3)
    db.session.commit()


def initCustomWord(db, CustomWord):
    w1 = CustomWord(
        word="input", length=5, language="English", email="admin@ics499.com", user_id=1
    )
    db.session.add(w1)
    w2 = CustomWord(
        word="output", length=6, language="English", email="admin@ics499.com", user_id=1
    )
    db.session.add(w2)

    w3 = CustomWord(
        word="తెలియకపోతే",
        length=6,
        language="Telugu",
        email="admin@ics499.com",
        user_id=1,
    )
    db.session.add(w3)
    w4 = CustomWord(
        word="ప్రతిభాసామర్ధ్యాల",
        length=7,
        language="Telugu",
        email="admin@ics499.com",
        user_id=1,
    )
    db.session.add(w4)
    w5 = CustomWord(
        word="test",
        length=4,
        language="English",
        email="ping@ics499.com",
        user_id=2,
    )
    db.session.add(w5)
    w6 = CustomWord(
        word="college",
        length=7,
        language="English",
        email="	ics499@gmail.com",
        user_id=3,
    )
    db.session.add(w6)
    w7 = CustomWord(
        word="matter",
        length=6,
        language="English",
        email="	ics325@gmail.com",
        user_id=4,
    )
    db.session.add(w7)
    w8 = CustomWord(
        word="gamer",
        length=5,
        language="English",
        email="	ics325@gmail.com",
        user_id=4,
    )
    db.session.add(w8)
    w9 = CustomWord(
        word="ఆరంభమవుతాయి",
        length=7,
        language="Telugu",
        email="	ics325@gmail.com",
        user_id=4,
    )
    db.session.add(w9)
    db.session.commit()


def initRecord(db, Record):
    r1 = Record(user_id=1, word="input", is_win=True, state="begin")
    db.session.add(r1)
    r2 = Record(user_id=1, word="output", is_win=False, state="streak")
    db.session.add(r2)
    db.session.commit()
    pass
