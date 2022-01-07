from app import db

class Board(db.Model):
    board_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    owner = db.Column(db.String)
    cards = db.relationship("Card", backref="card", lazy=True)

    COLUMNS = ["title", "owner"]

    def to_dict(self):
        return{
            "board_id" : self.board_id,
            "title" : self.title,
            "owner" : self.owner,
        }
    
    def board_w_cards_to_dict(self):
        return{
            "board_id" : self.board_id,
            "title" : self.title,
            "owner" : self.owner,
            "cards" : [card.card_to_dict_w_board() for card in self.cards]
        }
    
    @classmethod
    def from_dict(cls, values):
        columns = set(cls.COLUMNS)
        filtered = {k:v for k, v in values.items() if k in columns}
        return cls(**filtered)