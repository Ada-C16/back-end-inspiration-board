from app import db
from flask import current_app

class Board(db.Model):
    board_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    owner = db.Column(db.String)
    cards = db.relationship("Card", backref="board")

    def response_dict(self):
        board = Board.query.get(self.board_id)

        return {
            "title": self.title,
            "owner": self.owner
        }