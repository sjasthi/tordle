from flask import Flask, render_template, url_for, redirect, request
from utility.helper import *

app = Flask(__name__)
app.config["SECRET_KEY"] = "5791628bb0b13ce0c676dfde280ba245"
l = ["0", "1", "2", "add", "font", "clone", "telugu", "english", "absolute"]
params = {"length": 5, "attempt": 6, "language": "english"}
words = {"solution": l[5], "guess": ""}


@app.route("/", methods=["GET", "POST"])
def home():
    words["solution"] = l[int(request.args.get("length") or params["length"])]
    update_data(params, request, words)
    words["solution"] = l[params["length"]]
    print(params)
    print(words)
    return render_template("index.html", words=words, params=params)


# @app.route("/english", methods=["GET", "POST"])
# def english():
#     update_data(params, request, words)
#     words["solution"] = l[params["length"]]
#     print(words)
#     return render_template("index.html", words=words, params=params)


# @app.route("/telugu", methods=["GET", "POST"])
# def telugu():
#     words["solution"] = l[int(request.args.get("length") or params["length"])]
#     update_data(params, request, words, lang="telugu")
#     print(words)
#     return render_template("index.html", words=words, params=params)


if __name__ == "__main__":
    app.run(debug=True)
