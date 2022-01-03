from app import db

class Board(db.Model):
    board_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    owner = db.Column(db.String, nullable=False)
    card = db.relationship("Card", back_populates="board", lazy=True)

