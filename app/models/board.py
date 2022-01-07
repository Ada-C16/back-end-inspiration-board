from app import db


class Board(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    owner = db.Column(db.String)
    cards = db.relationship("Card", back_populates="board", lazy=True)
    required_fields = ["title", "owner"]

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "owner": self.owner,
        }
