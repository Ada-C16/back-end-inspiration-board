from flask import current_app
from app import db

class Board(db.Model):
    board_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    owner = db.Column(db.String)
    cards = db.relationship("Card", backref="card", lazy=True)

    def to_dict(self):
        return {
            "title": self.title,
            "owner": self.owner,
            "board_id": self.board_id
        }


    @classmethod
    def from_dict(cls, req):
        is_invalid_req = cls.check_invalid_req(req)
        if is_invalid_req:
            return is_invalid_req
        else:
            board = cls(
                title=req["title"],
                owner=req["owner"]
            )
            return board

    @staticmethod
    def check_invalid_req(req):
        if "title" not in req:
            return {
                "error": "Request body must contain title"
            }
        if "owner" not in req:
            return {
                "error": "Request body must contain owner"
            }
        return False

    
    # get_cards
    # checking id/getting board