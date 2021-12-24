from app import db


class Board(db.Model):
    board_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    owner = db.Column(db.String)
    card = db.relationship("Card", back_populates="board")

    def to_dict(self):
        response_body = {
            "board_id": self.board_id,
            "title": self.title,
            "owner": self.owner
        }
    
        # TODO: flesh this out later, if we want to list cards when reading boards
        # method would also take cards_list=None as a param
        #
        # if cards_list is not None:
        #     response_body["card"] = cards_list

        return response_body