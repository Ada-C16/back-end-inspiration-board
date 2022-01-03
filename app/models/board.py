from app import db


class Board(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(40))
    owner = db.Column(db.String(40))
    cards = db.relationship("Card", back_populates="board")