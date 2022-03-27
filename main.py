from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SECRET_KEY"] = "5791628bb0b13ce0c676dfde280ba245"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///words.db"
db = SQLAlchemy(app)
from helper import *


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
@app.route("/admin")
def admin():
    result = {
        "language": "English",
        "email": "",
        "pwd": "",
        "word_insert": "",
        "PASS": False,
    }
    if request.form:
        print("admin")
        print(request.form)
    # insert_word(request, result)
    return render_template("admin.html", result=result)


# admin@ics499.com -> ics499
@app.route("/admin", methods=["POST"])
def admin_input():
    print("admin_input")
    print(request.form)
    return render_template("admin.html")


@app.route("/my_word", methods=["GET", "POST"])
def my_input():
    return "Hello my_word!"


if __name__ == "__main__":
    app.run(debug=True)
