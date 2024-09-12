from app import db

class Card(db.Model):
    __tablename__= 'card'
    card_id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String)
    likes_count = db.Column(db.Integer)
    board_id_fk = db.Column(db.Integer, db.ForeignKey('board.board_id'), nullable=True)

    def to_dict(self):
        return {
            "id":self.card_id,
            "message": self.message,
            "likes" : self.likes_count
        }

#goal_id_fk = db.Column(db.Integer, db.ForeignKey('goals.goal_id'), nullable=True)

# Card, table name: card
# card_id, int, primary key
# message, string
# likes_count, int