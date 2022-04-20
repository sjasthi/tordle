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
    if current_user.is_authenticated:
        print(getStatics(current_user, params))
    return render_template("index.html", words=words, params=params)


@app.route("/", methods=["GET", "POST"])
def home():
    if current_user.is_authenticated:
        print(getStatics(current_user, params))
        if request.json:
            record = Record(
                user_id=current_user.id,
                word=request.json["answer"],
                is_win=request.json["is_win"],
                state="streak",
            )
            db.session.add(record)
            db.session.commit()
            print("Record: " + str(record))
    if request.form:
        if len(request.form) > 1:
            update_data(params, request, words)
        elif len(request.form) == 1 and params["language"] == "Telugu":
            words["word_input"] = request.form["word"]
            getResult(words)

    return render_template("index.html", words=words, params=params)


# admin@ics499.com -> ics499
@app.route("/admin/input_word")
@login_required
def admin():
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
    if current_user.role != "admin":
        return abort(403)
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
@login_required
def admin_input():
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
    if current_user.role != "admin":
        return abort(403)
    result = insert_word(request, db)
    params = {
        "length": len(result["word_insert"]) if not result["word_insert"] else 5,
        "attempt": 6,
        "language": "English",
        "url": None,
    }
    return render_template("admin.html", params=params, result=result)


@app.route("/my_word", methods=["GET"])
@login_required
def my_word():
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
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
@login_required
def my_word_post():
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
    result = generate_id(request, db, current_user)
    params = {
        "length": len(result["word_insert"]) if not result["word_insert"] else 5,
        "attempt": 6,
        "language": "English",
        "url": None,
    }
    return render_template("my_word.html", params=params, result=result)


@app.route("/my_word/<word_id>")
@login_required
def custom_word(word_id):
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
    result = get_word_by_id(word_id)
    if not result:
        return redirect(url_for("home"))
    if request.json:
        record = Record(
            user_id=current_user.id,
            word=request.json["answer"],
            is_win=request.json["is_win"],
            state="streak",
        )
        db.session.add(record)
        db.session.commit()
        print("Record: " + str(record))
    return render_template("index.html", words=result["words"], params=result["params"])


@app.route("/my_word/<int:word_id>", methods=["POST"])
@login_required
def custom_word_post(word_id):
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
    if request.form:
        if params["language"] == "Telugu":
            words["word_input"] = request.form["word"]
            getResult(words)
    if request.json:
        record = Record(
            user_id=current_user.id,
            word=request.json["answer"],
            is_win=request.json["is_win"],
            state="streak",
        )
        db.session.add(record)
        db.session.commit()
        print("Record: " + str(record))
    return render_template("index.html", words=words, params=params)


@app.route("/admin/custom_list", methods=["GET", "POST"])
@login_required
def custom_list():
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
    if current_user.role != "admin":
        return abort(403)
    result = get_custom_list(request)
    return render_template("custom_list.html", result=result, params=params)


@app.route("/admin/custom_list/<int:word_id>/delete", methods=["POST"])
@login_required
def delete_custom_word(word_id):
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
    if current_user.role != "admin":
        return abort(403)
    handle_delete_custom_word(request, word_id)
    return redirect(url_for("custom_list"))


@app.route("/admin/custom_list/edit", methods=["POST"])
@login_required
def edit_custom_word():
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
    if current_user.role != "admin":
        return abort(403)
    handle_edit_custom_word(request)
    return redirect(url_for("custom_list"))


@app.route("/admin/system_list", methods=["GET", "POST"])
@login_required
def system_list_search():
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
    if current_user.role != "admin":
        return abort(403)
    result = get_system_list_search(request)
    return render_template("system_list.html", result=result, params=params)


@app.route("/admin/system_list/<string:word>/delete", methods=["POST"])
@login_required
def delete_system_word(word):
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
    if current_user.role != "admin":
        return abort(403)
    handle_delete_word(word, request)
    return redirect(url_for("system_list_search"))


@app.route("/admin/system_list/edit", methods=["POST"])
@login_required
def edit_system_word():
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
    if current_user.role != "admin":
        return abort(403)
    handle_edit_word(request)
    return redirect(url_for("system_list_search"))


@app.route("/admin/register", methods=["GET", "POST"])
@login_required
def register():
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
    if current_user.role != "admin":
        return abort(403)
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            email=form.email.data, password=form.password.data, role=form.role.data
        )
        db.session.add(user)
        db.session.commit()
        flash(
            "The new User has been created! You are now able to log in with this one",
            "success",
        )
        return redirect(url_for("user_list"))
    return render_template(
        "register.html", title="Register", params=params, words=words, form=form
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("home"))
        else:
            flash("Login Unsuccessful. Please check email and password", "danger")
    return render_template(
        "login.html", title="Login", params=params, words=words, form=form
    )


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/admin/user_list", methods=["GET", "POST"])
@login_required
def user_list():
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
    if current_user.role != "admin":
        return abort(403)
    result = get_user_list(request)
    return render_template("user_list.html", result=result, params=params)


@app.route("/admin/user_list/<string:user_id>/delete", methods=["POST"])
@login_required
def delete_user(user_id):
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
    if current_user.role != "admin":
        return abort(403)
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash("The User has been deleted!", "success")
    return redirect(url_for("user_list"))


@app.route("/admin/user_list/edit", methods=["GET", "POST"])
@login_required
def edit_user():
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
    if current_user.role != "admin":
        return abort(403)
    handle_edit_user(request)
    return redirect(url_for("user_list"))
