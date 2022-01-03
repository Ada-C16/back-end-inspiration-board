from app import db


class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # board_id = db.Column(db.Integer, db.ForeignKey('board.id'))
    message = db.Column(db.String, nullable=False)
    like_count = db.Column(db.Integer, nullable=False)
    # board = db.relationship("Rental", back_populates="video", lazy=True)


    def to_dict(self):
        return {
            "id": self.id, 
            "board_id": self.board_id,
            "message": self.message,
            "like_count": self.like_count
        }
