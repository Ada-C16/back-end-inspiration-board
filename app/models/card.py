from app import db


class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.String(255), nullable=False)
    likes_count = db.Column(db.Integer, nullable=True)
    board = db.relationship("Board", back_populates="cards", lazy=True)
    board_id = db.Column(db.Integer, db.ForeignKey("board.id"))
    required_fields = ["message", "likes_count", "board_id"]

    def to_dict(self):
        return {
            "card_id": self.id,
            "message": self.message,
            "likes_count": self.likes_count,
            "board_id": self.board_id,
        }
