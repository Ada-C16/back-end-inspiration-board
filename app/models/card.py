from flask import current_app, abort
from app import db
from datetime import datetime, timezone


class Card(db.Model):
    card_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.String)
    likes_count = db.Column(db.Integer, default=0)
    board_id = db.Column(db.Integer, db.ForeignKey("board.board_id"))
    deleted_at = db.Column(db.DateTime, nullable=True, default=None)

    def to_dict(self):
        return {
            "message": self.message,
            "card_id": self.card_id,
            "likes_count": self.likes_count,
        }

    @classmethod
    def from_dict(cls, req, board_id):
        cls.check_invalid_req(req)
        card = cls(message=req["message"], board_id=board_id)
        return card

    @staticmethod
    def check_invalid_req(req):
        if "message" not in req:
            abort(400, "Request body must contain message")
        if not req["message"]:
            abort(400, "Card must have a non-empty message")
        if len(req["message"]) > 40:
            abort(400, "Type less than 40 characters for the message you fool")

    def add_like(self):
        if self.deleted_at:
            abort(400, "This card was already deleted")
        self.likes_count += 1
        return self

    def delete_card(self):
        self.deleted_at = datetime.now(timezone.utc)

    @classmethod
    def get_card(cls, id):
        try:
            int(id)
        except ValueError:
            abort(400, "Card ID must be a valid integer")

        card = cls.query.get_or_404(id)
        return card
