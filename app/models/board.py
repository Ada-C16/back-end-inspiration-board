from app import db

class Board(db.Model):

    model_type = "Board"
    board_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String) 
    owner = db.Column(db.String)

    def to_dict(self):
        """Returns model info as a dictionary."""
        return {
            "id": self.board_id,
            "title": self.title,
            "owner": self.owner
        }