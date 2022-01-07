from app import db
from flask import jsonify

class Board(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(40))
    owner = db.Column(db.String(40))
    cards = db.relationship("Card", backref="board")

    def read_cards(self):
        list_cards = []
        for card in self.cards:
            list_cards.append({"card_id": card.id, "message": card.message, "likes": card.likes})

        return {"title": self.title,
            "owner_name": self.owner,
            "cards": list_cards,
            "id": self.id
                   
        }

    def to_dict(self):
        return {
            "title": self.title,
            "owner_name": self.owner,
            "cards": self.read_cards(),
            "id": self.id
        }


