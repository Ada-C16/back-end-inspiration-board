from app import db

class Card(db.Model):
    card_id = db.Column(db.Integer, primary_key= True)
    title = db.Column(db.String)
    boards = db.relationship("Board", backref="Card", lazy = True)