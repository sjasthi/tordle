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

params = {"length": 5, "attempt": 6, "language": "english"}
words = {"solution": l[5], "guess": ""}

solution_tlg = getCharsFromAPI(telugus[0], "Telugu")
# ans = getResult(solution_tlg, guess_ts[3])
# print(ans)


@app.route("/", methods=["GET", "POST"])
def home():
    if request.form:
        print(request.form)
        if request.form["language"] == "English":
            words["solution"] = l[int(request.form["length"] or params["length"])]
            update_data(params, request, words)
            print(words)
        elif request.form["language"] == "Telugu":
            update_data(params, request, words)
            words["solution"] = getResult(solution_tlg, guess_ts[3])
            print(words)
    # words["solution"] = l[params["length"]]
    # print(params)
    # print(words)
    return render_template("index.html", words=words, params=params)


if __name__ == "__main__":
    app.run(debug=True)
