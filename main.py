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


if __name__ == "__main__":
    app.run(debug=True)
