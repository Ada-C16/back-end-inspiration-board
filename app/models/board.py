from app import db


class Board(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(40))
    owner = db.Column(db.String(40))
    cards = db.relationship("Card", backref="board")


def to_dict(self):

    return {
        "title": self.title,
        "owner_name": self.owner,
        "cards": self.cards,
    }

def read_cards(self):
    return self.cards