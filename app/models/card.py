from app import db


class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    likes = db.Column(db.Integer, default=None, nullable=True)
    message = db.Column(db.String(180))
    board = db.relationship("Board", back_populates="cards")
