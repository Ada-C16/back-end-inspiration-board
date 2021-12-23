from app import db
from app.models.card import Card

class Board(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(250), nullable=False)
    cards = db.relationship("Card", backref="board", lazy=True)