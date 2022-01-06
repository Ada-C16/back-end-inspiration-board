from app import db

class Card(db.Model):
    __tablename__ = "card"
    card_id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(40))
    likes_count = db.Column(db.Integer)
    board_id = db.Column(db.Integer, db.ForeignKey('board.board_id'))

    def to_dict(self):
        return {
            'card_id': self.card_id,
            'message': self.message,
            'likes_count': self.likes_count
        }