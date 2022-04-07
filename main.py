from flask import Flask, render_template, url_for, redirect, request, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SECRET_KEY"] = "5791628bb0b13ce0c676dfde280ba245"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///words.db"
db = SQLAlchemy(app)
from helper import *


@app.route("/")
def index():
    params = {
        "length": 5,
        "attempt": 6,
        "language": "English",
        "url": None,
    }
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
    return render_template("index.html", words=words, params=params)


@app.route("/", methods=["GET", "POST"])
def home():
    if request.form:
        if len(request.form) > 1:
            update_data(params, request, words)
        elif len(request.form) == 1 and params["language"] == "Telugu":
            words["word_input"] = request.form["word"]
            getResult(words)
    print(words)
    print(params)
    return render_template("index.html", words=words, params=params)


# admin@ics499.com -> ics499
@app.route("/admin/input_word")
def admin():
    result = {
        "language": "English",
        "email": "",
        "pwd": "",
        "word_insert": "",
        "PASS": False,
        "message": "",
    }
    params = {
        "length": 5,
        "attempt": 6,
        "language": result["language"],
        "url": None,
    }
    return render_template("admin.html", params=params, result=result)


# admin@ics499.com -> ics499
@app.route("/admin/input_word", methods=["POST"])
def admin_input():
    result = insert_word(request, db)
    params = {
        "length": len(result["word_insert"]) if not result["word_insert"] else 5,
        "attempt": 6,
        "language": "English",
        "url": None,
    }
    return render_template("admin.html", params=params, result=result)


@app.route("/my_word", methods=["GET"])
def my_word():
    result = {
        "language": "English",
        "email": "",
        "pwd": "",
        "word_insert": "",
        "PASS": False,
        "message": "",
    }
    params = {
        "length": 5,
        "attempt": 6,
        "language": result["language"],
        "url": None,
    }
    return render_template("my_word.html", params=params, result=result)


@app.route("/my_word", methods=["POST"])
def my_word_post():
    result = generate_id(request, db)
    params = {
        "length": len(result["word_insert"]) if not result["word_insert"] else 5,
        "attempt": 6,
        "language": "English",
        "url": None,
    }
    return render_template("my_word.html", params=params, result=result)


@app.route("/my_word/<word_id>")
def custom_word(word_id):
    result = get_word_by_id(word_id)
    if not result:
        return redirect(url_for("index"))
    return render_template("index.html", words=result["words"], params=result["params"])


@app.route("/my_word/<word_id>", methods=["POST"])
def custom_word_post(word_id):
    print(words, params)
    if request.form:
        if params["language"] == "Telugu":
            words["word_input"] = request.form["word"]
            getResult(words)
    return render_template("index.html", words=words, params=params)


@app.route("/admin/custom_list", methods=["GET", "POST"])
def custom_list():
    result = get_custom_list(request)
    return render_template("custom_list.html", result=result, params=params)


@app.route("/admin/system_list", methods=["GET", "POST"])
def system_list_search():
    result = get_system_list_search(request)
    return render_template("system_list.html", result=result, params=params)


if __name__ == "__main__":
    app.run(debug=True)
