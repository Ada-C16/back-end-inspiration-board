from flask import Blueprint, request, jsonify
from app import db
from app.models.card import Card
from app.models.board import Board


cards_bp = Blueprint("cards", __name__, url_prefix="/cards")
boards_bp = Blueprint("boards", __name__, url_prefix="/boards")

# each HTTP method should have it's own function to follow the single responsbility principle
@cards_bp.route("", methods=["GET"])
@cards_bp.route("/<board>/card")
def retrieve_cards():
    if request.method == 'GET':
        cards = Card.query.all()
        cards_response = []
        for card in cards:
            cards_response.append(card.card_dict())

        return jsonify(cards_response), 200


# CREATE
# Create a new board
@boards_bp.route("", methods=['POST'])
def create_board():
    request_body = request.getjson()
    if "name" not in request_body or "title" not in request_body:
        return jsonify("Not Found"), 404

    # 'name' represents "Owners name" in the form on the frontend
    new_board = Board(name=request_body["name"], title=request_body["title"])

    db.session.add(new_board)
    db.session.commit()

    return jsonify(f"Board: {new_board.name} successfully created."), 201


# Create a new card
@boards_bp.route("/<board_id>/cards", methods=['POST'])
#front-end needs a click event to provide API call to backend with board id
def create_card(board_id):
    board = Board.query.get(board_id)
    request_body = request.getjson()

    if "title" not in request_body or "message" not in request_body:
        return jsonify("Not Found"), 404

    # 'title' represents the Board's "Title"
    new_card = Card(title=request_body["title"], message=request_body["message"], likes_count=0)

    db.session.add(new_card)
    db.session.commit()

    return jsonify(f"Card for board: {new_card.title} successfully created."), 201



# READ
# All cards within a board
# @cards_bp.route("", methods=["GET"])
@boards_bp.route("/<board_id>/cards", methods=['GET'])
def retrieve_cards(board_id):
    board = Board.query.get(board_id)
    cards_response = [card.card_dict() for card in board.cards]

    return jsonify(cards_response), 200


# All boards (board names) listed on Inspiration Board

# UPDATE
# Can update cards by adding 'likes'
@cards_bp.route("/<card_id>", methods=["PATCH"])
def update_card(card_id):
    card = Card.query.get(card_id)
    if card is None:
        return jsonify("Not Found"), 404

    card.likes_count += 1

    db.session.commit()

    return jsonify(f"Card {card.id} successfully updated"), 200


# DELETE

# Can delete a single board


@boards_bp.route("/<board_id>", methods=["DELETE"])
def delete_board(board_id):
    board = Board.query.get(board_id) 
    # cards = #Card.query.get(board.cards) does this return card object or id(OBJECT IS BETTER)
    # cascading delete 

    # for card in cards:
    for card in board.cards:
        db.session.delete(card)
        #db.session.commit()
    db.session.delete(board)
    db.session.commit()
# Can delete cards in a board
@boards_bp.route("/<card_id>", methods=["DELETE"])
def delete_card(card_id):
    card = Board.query.get(card_id) 
    # cards = Card.query.get(board.cards) does this return card object or id(OBJECT IS BETTER)

    db.session.delete(card)
    db.session.commit()

    return jsonify({f"Card {card} successfully deleted."})



# added back
@cards_bp.route("/<card_id>", methods= ["GET", "PUT","DELETE"])
def retrieve_get_card(card_id):
    card = Card.query.get(card_id)
    if "card" is None: 
        return jsonify(None), 404
    elif request.method == "GET":
        pass
    elif request.method == "PUT":
        pass

    elif request.method == "DELETE":
        db.session.delete(card)
        db.session.commit()

        return {
            "message": (f"Card {card_id} has been deleted")
        }


#Delete created and needs to be modified.    
@boards_bp.route("/<board_id>", methods=["DELETE"])
def delete_board(board_id):
    board = Board.query.get(board_id) 
    # cards = #Card.query.get(board.cards) does this return card object or id(OBJECT IS BETTER)

    # for card in cards:
    for card in board.cards:
        db.session.delete(card)
    db.session.delete(board_id)
    db.session.commit()