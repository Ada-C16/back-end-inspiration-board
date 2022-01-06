from flask import current_app, abort
from app import db


class Board(db.Model):
    board_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    owner = db.Column(db.String)
    cards = db.relationship("Card", backref="card", lazy=True)

    def to_dict(self):
        return {"title": self.title, "owner": self.owner, "board_id": self.board_id}

    @classmethod
    def from_dict(cls, req):
        cls.check_invalid_req(req)
        board = cls(title=req["title"], owner=req["owner"])
        return board

    @staticmethod
    def check_invalid_req(req):
        if "title" not in req:
            abort(400, "Request body must contain title")
        if "owner" not in req:
            abort(400, "Request body must contain owner")
        if not req["title"]:
            abort(400, "Board must have a non-empty title")
        if not req["owner"]:
            abort(400, "Board must have a non-empty owner")

    def get_all_cards(self):
        return [card.to_dict() for card in self.cards if not card.deleted_at]

    @classmethod
    def get_board(cls, id):
        try:
            int(id)
        except ValueError:
            abort(400, "Board ID must be a valid integer")
        board = cls.query.get_or_404(id)
        return board
