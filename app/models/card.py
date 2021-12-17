from app import db

class Card(db.Model):
    card_id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text, db.ForeignKey)
    likes_count = db.Column(db.Integer, db.ForeignKey)