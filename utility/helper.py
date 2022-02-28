def update_data(params, request, words, lang="english"):
    params["length"] = int(request.form["length"] or params["length"])
    params["attempt"] = int(request.form["attempt"] or params["attempt"])
    params["language"] = (request.form["language"]).lower() or params["language"]
    words["guess"] = request.form.get("word") or words["guess"]
