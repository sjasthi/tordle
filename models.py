import random
from main import db


class English(db.Model):
    word = db.Column(db.String(100), primary_key=True)
    length = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f"English(word:'{self.word}', length:{self.length})"


class Telugu(db.Model):
    word = db.Column(db.String(500), primary_key=True)
    length = db.Column(db.Integer, nullable=True)
    list_str = db.Column(db.String(5000), unique=True, nullable=True)

    def __repr__(self):
        return f"Telugu(word:'{self.word}', length:{self.length}, list_str:'{self.list_str}')"


class User(db.Model):
    email = db.Column(db.String(500), primary_key=True)
    pwd = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"User(Email:'{self.email}', Password:'{self.pwd}')"


class CustomWord(db.Model):
    id = db.Column(
        db.Integer, db.Sequence("seq_reg_id", start=1000, increment=1), primary_key=True
    )
    word = db.Column(db.String(500), nullable=False)
    length = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(500), nullable=False)
    language = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        return f"CustomWord(id:'{self.id}', Word:'{self.word}', \
            Email:'{self.email}', Language:'{self.language}')"


def getRandomWordByLength(length, language):
    if language == "English":
        results = English.query.filter_by(length=length).all()
        result = random.choice(results)
        return result.word
    elif language == "Telugu":
        results = Telugu.query.filter_by(length=length).all()
        result = random.choice(results)
        return result
