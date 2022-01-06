from app import db

class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    board_id = db.Column(db.Integer, db.ForeignKey('board.id'), nullable=False)
    value = db.Column(db.String, nullable=False)
    num_likes = db.Column(db.Integer, default=0)
    date = db.Column(db.Date)

    @classmethod
    def validate_data(cls, dict):
        # Validates the data input by the user
        types = {
            "text": str
        }
        for input_type in types:
            if not dict.get(input_type):
                return False
            if type(dict.get(input_type)) != types[input_type]:
                return False
        return True
    
