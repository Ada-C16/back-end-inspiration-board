from app import db

class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    board_id = db.Column(db.Integer, db.ForeignKey('board.id'), nullable=False)
    value = db.Column(db.String, nullable=False)
    num_likes = db.Column(db.Integer, default=0)
    date = db.Column(db.Date)
    
