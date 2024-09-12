from app import db

class Board(db.Model):
    __tablename__= 'board'
    board_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    owner = db.Column(db.String)
    cards = db.relationship('Card', backref='board')


    def to_dict(self):
        return {"board_id": self.board_id,
            "title": self.title,
            "owner": self.owner,
            # "cards":[card.to_dict() for card in self.cards],
            }


#tasks = db.relationship('Task', backref='goal', lazy=True)