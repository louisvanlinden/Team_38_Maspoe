from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "User"  # matcht je Supabase-tabel
    id = db.Column(db.BigInteger, primary_key=True)
    email = db.Column(db.Text, nullable=True)

class Artists(db.Model):
    __tablename__ = "Artists"
    id = db.Column(db.BigInteger, primary_key=True)
    Artist_name = db.Column(db.Text, nullable=False)

class FestivalEdition(db.Model):
    __tablename__ = "FestivalEdition"
    id = db.Column(db.BigInteger, primary_key=True)
    Start_date = db.Column(db.Date)
    End_date = db.Column(db.Date)
    Name = db.Column(db.Text, nullable=False)
    Location = db.Column(db.Text, nullable=True)

class Poll(db.Model):
    __tablename__ = "poll"
    id = db.Column(db.BigInteger, primary_key=True)
    Question = db.Column(db.Text, nullable=False)
    festival_id = db.Column(db.BigInteger, db.ForeignKey("FestivalEdition.id"), nullable=False)
    festival = db.relationship(FestivalEdition, backref="polls")

class Polloption(db.Model):
    __tablename__ = "Polloption"
    id = db.Column(db.BigInteger, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    artist_id = db.Column(db.BigInteger, db.ForeignKey("Artists.id"), nullable=True)
    poll_id = db.Column(db.BigInteger, db.ForeignKey("poll.id"), nullable=False)
    poll = db.relationship(Poll, backref="options")
    artist = db.relationship(Artists)

class VotesFor(db.Model):
    __tablename__ = "Votes_for"
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    user_id = db.Column(db.BigInteger, db.ForeignKey("User.id"), primary_key=True)
    polloption_id = db.Column(db.BigInteger, db.ForeignKey("Polloption.id"), primary_key=True)
    option = db.relationship(Polloption)
    user = db.relationship(User)

class SuggestionFeedback(db.Model):
    __tablename__ = "Suggestion_feedback"
    id = db.Column(db.BigInteger, primary_key=True)
    artist_id = db.Column(db.BigInteger, db.ForeignKey("Artists.id"), nullable=True)
