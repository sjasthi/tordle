def update_data(params, request, words, lang="english"):
    params["length"] = int(request.args.get("length") or params["length"])
    params["attempt"] = int(request.args.get("attempt") or params["attempt"])
    params["language"] = lang
    words["guess"] = request.form.get("word") or words["guess"]
