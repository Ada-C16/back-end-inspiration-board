from app import db
from app.models.card import Card
MAX_NAME_LENGTH = 250


class Board(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(MAX_NAME_LENGTH), nullable=False)
    cards = db.relationship("Card", backref="board", lazy=True)

    def get_all_stickies(self):
        stickies = []

        for sticky in self.cards:
            stickies.append({
                "id": sticky.id,
                "text": sticky.value,
                "num_likes": sticky.num_likes,
                "date": sticky.date.strftime('%b %w, %Y')
            })
        sorted_stickies = sorted(stickies, key = lambda i: i['id'])
        return sorted_stickies

    @classmethod
    def validate_data(cls, dict):
        # Validates the data input by the user
        types = {
            "name": str
        }
        for input_type in types:
            if not dict.get(input_type):
                return False
            if type(dict.get(input_type)) != types[input_type]:
                return False
        if len(dict["name"]) > MAX_NAME_LENGTH:
            return False
        return True