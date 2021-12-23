from app import db

class Card (db.Model):
    card_id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String)
    likes_count = db.Column(db.Integer, default=0)
    board_id = db.Column(db.Integer, db.ForeignKey('board.board_id'))
    board = db.relationship("Board", back_populates="cards")

    def update_likes(self):
        self.likes_count += 1
        # return self.likes_count

    def update_attributes(self, board_id, request_body):
        self.board_id = board_id
        self.message=request_body["message"]

    def card_details(self):
        return {
            "card_id": self.card_id,
            "message": self.message,
            "likes_count": self.likes_count,
            "board_id": self.board_id
        }