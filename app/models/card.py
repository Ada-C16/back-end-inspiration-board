from app import db
from sqlalchemy.orm import backref

class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.String)
    likes_count = db.Column(db.Integer)
    board_id = db.Column(db.Integer, db.ForeignKey("board.id"), nullable=False)
    boards = db.relationship("Board", backref=backref("boards", cascade="delete"))

    def to_json(self):
        return {
            "id" : self.id,
            "message" : self.message,
            "likes_count" : self.likes_count,
            "board_id" : self.board_id
        }