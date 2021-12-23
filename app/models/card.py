from app import db

# Child class
# A card belongs to one board
class Card(db.Model):
    card_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.String)
    likes_count = db.Column(db.Integer, default = 0)
    board_id = db.Column(db.Integer, db.ForeignKey("board.board_id"))
    # ^^ board_id = db.column(db.Integer, db.ForeignKey("board.board_id"))
    # since we use backref on the parent class we dont need to reiterate the relationship
    # on the child class & we identify the board via it's id (the FK)

    def card_dict(self):
        return {
            "id": self.card_id,
            "message": self.message,
            "likes_count": self.likes_count
        }