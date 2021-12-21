from app import db
# card needs id, message, increase_likes
# building the database table with columns, data type, column names
class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.String)
    increase_likes = db.Column(db.Integer)