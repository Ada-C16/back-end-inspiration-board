from app import db
# card needs id, message, increase_likes
# building the database table with columns, data type, column names
class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.String)
    likes = db.Column(db.Integer)
    board_id = db.Column(db.Integer, db.ForeignKey('board.id'), nullable=False)
    # this relationship establishes a new attribute for each Card object, which allows it to access the Board object
    # through Card.board and a second new attribute, Board.cards (plural bc each Board has multiple Cards)
    board =db.relationship('Board', backref='cards')
# this helper function takes a Card object and returns it as a JSON object/ dict
    def convert_to_dict(self):
        return { "id": self.id,
                "message": self.message,
                "likes": self.likes}

