from flask import current_app
from app import db

class Card(db.Model):
    card_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.String)
    likes_count = db.Column(db.Integer, default=0)
    board_id = db.Column(db.Integer, db.ForeignKey('board.board_id'))
    deleted = db.Column(db.Boolean, default=False)
    deleted_at = db.Column(db.DateTime, nullable=True, default=None)

    # to_dict
    def to_dict(self):
        return {
            "message": self.message,
            "card_id": self.card_id,
            "likes_count": self.card_id
        }
    # from_dict
    # liking
    # checking card_id
    # delete card