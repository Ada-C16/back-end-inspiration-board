from flask import Blueprint, request, jsonify
from app import db
from app.models.board import Board
from app.models.card import Card


cards_bp = Blueprint("cards", __name__, url_prefix="/cards")
boards_bp = Blueprint("boards", __name__, url_prefix="/boards")


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