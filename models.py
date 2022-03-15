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


def getRandomWordByLength(length, language):
    if language == "English":
        results = English.query.filter_by(length=length).all()
        result = random.choice(results)
        return result.word
    elif language == "Telugu":
        results = Telugu.query.filter_by(length=length).all()
        result = random.choice(results)
        return result
