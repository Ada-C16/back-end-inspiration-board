from flask import current_app
from app import db

class Board(db.Model):
    board_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    owner = db.Column(db.String)
    cards = db.relationship("Card", backref="card", lazy=True)

    # to_dict
    # from_dict
    # get_cards
    # checking id/getting board