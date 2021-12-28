from app import db

class Card(db.Model):
    card_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.String)
    likes_count = db.Column(db.Integer)

    def to_dict(self):
        card = {
            "id" : self.card_id,
            "message" : self.message,
            "likes_count" : self.likes_count
        }

        return card

    @classmethod
    def from_dict(cls, request_body):
        card = Card(
            message=request_body["message"],
            likes_count=request_body["likes_count"]
        )

        return card 
