"""Author: Nalongsone Danddank, Assignment #4, Feb 2 2022, ICS499 METRO STATE """

import requests
import json


def update_data(params, request, words, lang="english"):
    params["length"] = int(request.form["length"] or params["length"])
    params["attempt"] = int(request.form["attempt"] or params["attempt"])
    params["language"] = (request.form["language"]).lower() or params["language"]
    words["guess"] = request.form.get("word") or words["guess"]


def getCharsFromAPI(string, language):
    """@string: String for api params
    @language: String for api params"""
    URL_char = "https://indic-wp.thisisjava.com/api/getLogicalChars.php"
    URL_len = "https://indic-wp.thisisjava.com/api/getLength.php"
    params = {"string": string, "language": language}
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
    }
    # get text or string that request from API
    r_chars = requests.get(url=URL_char, params=params, headers=headers, timeout=5)
    # handle text like json format from api by encode and decode the string.
    text = r_chars.text
    if text.startswith("\ufeff"):
        text = text.encode("utf8")[6:].decode("utf8")
    # convert text to dictionary by json
    data = json.loads(text)

    # get chars length from API
    r_len = requests.get(url=URL_len, params=params, headers=headers, timeout=5)
    text = r_len.text
    if text.startswith("\ufeff"):
        text = text.encode("utf8")[6:].decode("utf8")
    len_json = json.loads(text)
    # return both chars list and its length
    return data["data"], len_json["data"]
