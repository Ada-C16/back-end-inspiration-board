from app import db

class Card(db.Model):
    card_id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String)
    likes_count = db.Column(db.Integer)
    board_id = db.Column(db.Integer, db.ForeignKey('board.id'), nullable=True)

    COLUMNS = ["message"]

    def to_dict(self):
        return {
            "card_id": self.card_id,
            "message": self.message,
            "likes_count" : self.likes_count
        }
    def card_to_dict_w_goal(self):
        return {
            "card_id": self.card_id,
            "message": self.message,
            "likes_count" : self.likes_count,
            "board_id" : self.board_id
        }
    @classmethod
    def from_dict(cls, values):
        columns = set(cls.COLUMNS)
        filtered = {k:v for k, v in values.items() if k in columns}
        return cls(**filtered)