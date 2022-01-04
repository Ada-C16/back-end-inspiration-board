from app import db

class Board(db.Model):
    board_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    owner = db.Column(db.String, nullable=False)
    card = db.relationship("Card", back_populates="board", lazy=True)

    def to_dict(self):
        return {
            "id": self.board_id,
            "title": self.title,
            "owner": self.owner
        }

    def to_dict_with_cards(self):
        result = []
        for cards in self.card:
            result.append({
                "id": cards.id, 
                "board_id": self.board_id,
                "message": cards.message,
                "like_count": cards.like_count
                }        
            )
