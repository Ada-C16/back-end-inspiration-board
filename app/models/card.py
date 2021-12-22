from app import db
from flask import current_app


class Card(db.Model):
    # rename to just id on both models - from Ansel
    card_id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String)
    likes_count = db.Column(db.Integer, default=0)
    board_id = db.Column(db.Integer, db.ForeignKey(
        'board.board_id'), nullable=False)

    def create_card_dict(self):
        return_dict = {
            "id": self.card_id,
            "message": self.message,
            "likes_count": self.likes_count,
            "board_id": self.board_id
        }
        return return_dict
