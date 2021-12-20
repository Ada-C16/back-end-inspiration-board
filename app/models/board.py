from app import db
# board needs id, title, author
# building the database table with columns, data type, column names
class Board(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    author= db.Column(db.String)