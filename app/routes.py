from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.board import Board
from app.models.card import Card

# example_bp = Blueprint('example_bp', __name__)
cards_bp = Blueprint("cards", __name__, url_prefix="/cards")
boards_bp = Blueprint("boards", __name__, url_prefix="/boards")


# CREATE
# A new board
@boards_bp.route("", methods=['POST'])
def create_board():
    request_body = request.getjson()
    if "name" not in request_body or "title" not in request_body:
        return jsonify("Not Found"), 404

    # name represents "Owners name" in the form on the frontend
    new_board = Board(name=request_body["name"], title=request_body["title"])

    db.session.add(new_board)
    db.session.commit()

    return jsonify(f"Board: {new_board.name} successfully created."), 201


#  Create a new card within a board
@boards_bp.route("/<board_id>/cards", methods=['POST'])
def create_card(board_id):
    board = Board.query.get(board_id)
    if board is None:
        return jsonify("Not Found"),404

    request_body = request.getjson()
    card_ids = request_body["card_ids"]

    for card_id in card_ids:
        card = Card.query.get(card_id)
        card.board_id = int(board_id)

    new_cards = []
    for card in board.cards:
        new_cards.append(card.card_id)
    # 'new cards' should return all newly created cards within a specific board  
    response_body = {
        "id": board.board_id,
        "card_ids": new_cards,  
    }

    db.session.commit()

    return jsonify(response_body), 200





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