from flask import current_app
from app import db
from datetime import datetime, timezone

class Card(db.Model):
    card_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.String)
    likes_count = db.Column(db.Integer, default=0)
    board_id = db.Column(db.Integer, db.ForeignKey('board.board_id'))
    deleted = db.Column(db.Boolean, default=False)
    deleted_at = db.Column(db.DateTime, nullable=True, default=None)

    def to_dict(self):
        return {
            "message": self.message,
            "card_id": self.card_id,
            "likes_count": self.likes_count
        }

    @classmethod
    def from_dict(cls, req, board_id):
        is_invalid_req = cls.check_invalid_req(req)
        if is_invalid_req:
            return is_invalid_req
        else:
            card = cls(
                message=req["message"],
                board_id=board_id
            )
            return card

    @staticmethod
    def check_invalid_req(req):
        if "message" not in req:
            return {"error": "Request body must contain message"}
        return False 

    
    def add_like(self):
        self.likes_count += 1
        return self.to_dict()

    
    def delete_card(self):
        self.deleted_at = datetime.now(timezone.utc)
    
    @classmethod
    def get_card(cls, id):
        try:
            int(id)
        except ValueError:
            return False
        card = cls.query.get_or_404(id)
        return card
