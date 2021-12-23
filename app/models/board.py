from app import db
# board needs id, title, author
# building the database table with columns, data type, column names
class Board(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    author= db.Column(db.String)

    # this helper function takes a Board object and returns it as a JSON object/ dict
    def convert_board_to_dict(self):
        return { "id": self.id,
                "title": self.title,
                "author": self.author}