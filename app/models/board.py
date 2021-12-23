from app import db


class Board(db.Model):
    __tablename__ = "Board"
    board_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    owner = db.Column(db.String)