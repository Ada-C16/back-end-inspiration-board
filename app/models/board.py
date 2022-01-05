from app import db
from sqlalchemy.orm import backref

class Board(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    owner_name = db.Column(db.String)
    title = db.Column(db.String)

    # RETURNS RESPONSE BODY
    def get_board_response(self):
        return {
            "id": self.id,
            "owner_name": self.owner_name,
            "title": self.title,
        }  
