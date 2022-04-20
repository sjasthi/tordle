from routes import *


def setup_db():
    # db.drop_all()
    # db.session.commit()

    # db.create_all()
    # db.session.commit()

    # englishFile2db("db/english.txt", db, English)
    # teluguFile2db("db/telugu.txt", db, Telugu)
    # initUser(db, User)
    # initCustomWord(db, CustomWord)
    # initRecord(db, Record)
    pass


if __name__ == "__main__":
    # setup_db()
    app.run(debug=True)
