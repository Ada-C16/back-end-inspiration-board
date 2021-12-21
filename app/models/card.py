from app import db
# card needs id, message, increase_likes
# building the database table with columns, data type, column names
class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.String)
    increase_likes = db.Column(db.Integer)
# this helper function takes a Card object and returns it as a JSON object/ dict
    def convert_to_dict(self):
        return { "id": self.id,
                "message": self.message,
                "increase_likes": self.increase_likes}
                                        