from app import db

class Card(db.Model):
    card_id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String)
    likes_count = db.Column(db.Integer)
    board_id = db.Column(db.Integer, db.ForeignKey('board.board_id'), nullable=False)

    def to_dict(self):
        card = {
            "id" : self.card_id,
            "message" : self.message,
            "likes_count" : self.likes_count
        }

        return card

    @classmethod
    def from_dict(cls, request_body):
        card = Card(
            board_id=request_body["board_id"],
            message=request_body["message"],
            likes_count=request_body["likes_count"]
        )

        return card 
