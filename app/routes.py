from flask import Blueprint, request, jsonify
from app import db
from app.models.card import Card
from app.models.board import Board
from app.models.board import Board
from app.models.card import Card

cards_bp = Blueprint("cards", __name__, url_prefix="/cards")
boards_bp = Blueprint("boards", __name__, url_prefix="/boards")

@cards_bp.route("", methods=["GET","POST"])
def retrieve_cards():
    if request.method == 'GET':
        cards = Card.query.all()
        cards_response = []
        for card in cards:
            cards_response.append(card.card_dict())

        return jsonify(cards_response), 200

    elif request.method == "POST":
        request_body = request.get_json()
        if "message" not in request_body or "likes_count" not in request_body:
            return jsonify ({
                "error meesage": "Invalid data"
            }), 400
        new_card = Card(
            message = request_body["message"],
            likes_count = request_body["likes_count"]
        )

        db.session.add(new_card)
        db.session.commit()

        response_body ={"card": new_card.card_dict()}
        return jsonify(response_body),201

        @cards_bp.route("/<card_id>", methods= ["GET", "PUT","DELETE"])
        def retrieve_get_card(card_id):
            if card is None: 
                return jsonify(None), 404
            elif request.method == "GET":
                

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
@cards_bp.route("", methods=['POST'])
def create_card():
    request_body = request.getjson()

    # 'likes_count by default will be 0 for every new card. Curious how we can hard card this in
    # so it's not a required request parameter
    if "title" not in request_body or "message" not in request_body or "likes_count" not in request_body:
        return jsonify("Not Found"), 404

    # 'title' represents the Board's "Title"
    new_card = Card(title=request_body["title"], message=request_body["message"], likes_count=request_body["likes_count"])

    db.session.add(new_card)
    db.session.commit()

    return jsonify(f"Card for board: {new_card.title} successfully created."), 201





# READ
# All cards within a board
# All boards (board names) listed on Inspiration Board

# UPDATE
# Can update a board by adding new cards
# Can update cards by adding 'likes'

# DELETE
# Can delete cards in a board
# Can delete a single board
# Can delete all cards and boards (? do we want to include this functionality?)
