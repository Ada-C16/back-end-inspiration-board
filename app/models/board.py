from app import db

# Parent class
# One board can have many cards
class Board(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    owner = db.Column(db.String)
    cards = db.relationship("Card", backref="cards", lazy = True)
    # ^^ cards = db.relationship("Card", backref="Board", lazy = True)

    def board_dict(self):
        return{
            "id": self.id,
            "title": self.title,
            "owner": self.owner
        }