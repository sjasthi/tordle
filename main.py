from flask import Flask, render_template, url_for, redirect, request
from utility.helper import *


app = Flask(__name__)
app.config["SECRET_KEY"] = "5791628bb0b13ce0c676dfde280ba245"
l = ["0", "1", "2", "add", "font", "clone", "telugu", "english", "absolute"]
telugus = ["సిరివెన్నెల"]
guess_ts = [
    "తమిళభాష",
    "సిరివెన్నెల",
    "వెన్నెలరేడు",
    "వెన్నెలకాడు",
    "సరేవీనీలా",
    "వానలసిరి",
]

params = {"length": 5, "attempt": 6, "language": "English"}
words = {
    "solution": l[5],
    "result": [],
    "word_input": "",
    "wordCount": 0,
    "word_len_test": False,
}


@app.route("/", methods=["GET", "POST"])
def home():
    if request.form:
        if len(request.form) > 1:
            if request.form["language"] == "English":
                words["solution"] = l[int(request.form["length"] or params["length"])]
                update_data(params, request, words)
            elif request.form["language"] == "Telugu":
                update_data(params, request, words)
                words["solution"] = getCharsFromAPI(telugus[0], "Telugu")
        elif len(request.form) == 1 and params["language"] == "Telugu":
            if request.form["word"] != "":
                words["word_input"] = request.form["word"]
                getResult(words)

    print(words)
    print(params)
    return render_template("index.html", words=words, params=params)


if __name__ == "__main__":
    app.run(debug=True)
