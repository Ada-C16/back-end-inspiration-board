from app import db


class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    board_id = db.Column(db.Integer, db.ForeignKey("board.id"), nullable=True)
    likes = db.Column(db.Integer, default=None, nullable=True)
    message = db.Column(db.String(180))



