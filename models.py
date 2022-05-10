"""Author: Nalongsone Danddank, Final Project, begin on Feb 2 2022, end on April 27, 2022, ICS499 METRO STATE """
from config import *


class English(db.Model):
    word = db.Column(db.String(100), primary_key=True)
    length = db.Column(db.Integer, nullable=True)
    latest_play_time = db.Column(db.DateTime)

    def __repr__(self):
        return f"English(word:'{self.word}', length:{self.length},\
            latest_play_time:'{self.latest_play_time}')"


class Telugu(db.Model):
    word = db.Column(db.String(500), primary_key=True)
    length = db.Column(db.Integer, nullable=True)
    latest_play_time = db.Column(db.DateTime)

    def __repr__(self):
        return f"Telugu(word:'{self.word}', length:{self.length},\
            latest_play_time:'{self.latest_play_time}')"


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(500), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False, default="member")
    create_time = db.Column(db.DateTime, default=datetime.utcnow)
    custom_words = db.relationship(
        "CustomWord",
        backref=db.backref("user", lazy=True),
    )
    records = db.relationship("Record", backref=db.backref("user", lazy=True))

    def __repr__(self):
        return f"User(Id:'{self.id}', Email:'{self.email}', Password:'{self.password}',\
            Role:'{self.role}', Create Time: '{self.create_time}', Custom Word List:'{self.custom_words}')"


class CustomWord(db.Model):
    __tablename__ = "custom_word"
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(500), unique=True, nullable=False)
    length = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(500), nullable=False)
    language = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"CustomWord(id:'{self.id}', Word:'{self.word}', \
            Email:'{self.email}', Language:'{self.language}',\
                User Id:'{self.user_id}' Create Time: '{self.create_time}')"


class Record(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"), nullable=False)
    word = db.Column(db.String(500), nullable=False)
    is_win = db.Column(db.Boolean(), default=False)
    state = db.Column(db.String(50))
    attempt_time = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Record(Id:'{self.id}', User Id:'{self.user_id}', Word:'{self.word}',\
            Is Win:'{self.is_win}', State:'{self.state}', Attempt Time:'{self.attempt_time}')"
