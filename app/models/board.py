from sqlalchemy.orm import backref
from app import db

class Board(db.Model):
    board_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    owner = db.Column(db.String, nullable=False)
    cards =  db.relationship('Card', backref='board', lazy='dynamic', cascade='all,delete-orphan')

    def make_board_json(self):
        return {
                "board id": self.board_id,
                "title": self.title,
                "owner": self.owner
        }