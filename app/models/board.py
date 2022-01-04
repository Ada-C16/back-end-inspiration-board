from app import db
from app.models.card import Card

class Board(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(250), nullable=False)
    cards = db.relationship("Card", backref="board", lazy=True)

    def get_all_stickies(self):
        stickies = []

        for sticky in self.cards:
            stickies.append({
                "id": sticky.id,
                "text": sticky.value,
                "num_likes": sticky.num_likes,
                "date": sticky.date
            })

        return stickies