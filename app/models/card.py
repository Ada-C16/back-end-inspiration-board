from app import db


class Card(db.Model):
    __tablename__ = "Card"
    card_id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String)
    likes_count = db.Column(db.Integer)