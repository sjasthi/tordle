from flask import Flask, render_template, url_for, redirect, request
from utility.helper import *


app = Flask(__name__)
app.config["SECRET_KEY"] = "5791628bb0b13ce0c676dfde280ba245"
l = ["0", "1", "2", "add", "font", "clone", "telugu", "english", "absolute"]
telugus = ["సిరివెన్నెల"]
guess_ts = [
    "తమిళభాష",
    "సిరివెన్నెల",
    "సరేవీనీలా",
    "వానలసిరి",
    "వెన్నెలకాడు",
    "వెన్నెలరేడు",
]

params = {"length": 5, "attempt": 6, "language": "english"}
words = {"solution": l[5], "guess": ""}

# tt = getCharsFromAPI(telugus[0], "Telugu")
# print(tt)
# test = getCharsFromAPI(guess_ts[3], "Telugu")
# print(test)
# result = ""
# if tt[1] == test[1]:
#     for i in range(tt[1]):
#         if tt[0][i] == test[0][i]:
#             result += "1"
#         else:
#             result += "0"
# print(result)
# # utf8 = chr(38)
# # ns = utf8.encode("utf8")
# bi = "రి"[0]
# # bi = r"{}".format(bii)
# print(bi)
# print("\u0c38\u0c3f\u0c30\u0c3f\u0c35")


@app.route("/", methods=["GET", "POST"])
def home():
    if request.form:
        print(request.form)
        if request.form["language"] == "english":
            words["solution"] = l[int(request.form["length"] or params["length"])]
            update_data(params, request, words)
        else:
            pass
    words["solution"] = l[params["length"]]
    print(params)
    print(words)
    return render_template("index.html", words=words, params=params)


if __name__ == "__main__":
    app.run(debug=True)
