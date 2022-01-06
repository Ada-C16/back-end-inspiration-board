from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.board import Board
from app.models.card import Card

# example_bp = Blueprint('example_bp', __name__)

board_bp = Blueprint("board", __name__, url_prefix="/boards")
card_bp = Blueprint("card", __name__, url_prefix="/cards")

# Helper function to validate the board request
def validate_board(request_body):
    if "title" not in request_body or "owner" not in request_body:
        return jsonify({"details": "Request body must include title and author"}), 400

# Board routes:
# Get all Boards
@board_bp.route("", methods=["GET"])
def get_all_boards():
    boards = Board.query.all()
    board_list = []
    for board in boards:
        board_list.append(board.to_dict())
    return jsonify(board_list), 200

# Get single a single board
@board_bp.route("/<board_id>", methods=["GET"])
def get_single_board(board_id):
    board = Board.query.get(board_id)
    if board:
        return board.to_dict(), 200
    else:
        return jsonify({"This board does not exist, make a board"}), 404

# Post a board
@board_bp.route("", methods=["POST"])
def create_a_board():
    request_body = request.get_json()

    validate_board(request_body)

    new_board = Board(title=request_body["title"],
    owner=request_body["owner"]
    )

    db.session.add(new_board)
    db.session.commit()

    return jsonify(new_board.to_dict()), 201

# Update a board
@board_bp.route("/<board_id>", methods=["PUT"])
def update_board(board_id):
    board_id = int(board_id)
    board = Board.query.get(board_id)
    form_data = request.get_json()

    if board:
        board.title = form_data["title"]
        board.owner = form_data["owner"]
        db.session.commit()
        return jsonify(board.to_dict()), 200
    else:
        return jsonify("Invalid data"), 404

# Delete a board
@board_bp.route("/<board_id>", methods=["DELETE"])
def delete_board(board_id):
    board_id = int(board_id)
    board = Board.query.get(board_id)

    if board:
        db.session.delete(board)
        db.session.commit()
        return jsonify("Board was succesfully deleted"), 200
    else:
        return jsonify("Board does not exist"), 404

# Card Routes:
# Get cards for board id
@board_bp.route("/<board_id>/cards", methods=["GET"])
def get_cards_for_board(board_id):
    board_id = int(board_id)
    board = Board.query.get(board_id)
    if board:
        cards = Card.query.filter_by(board_id=board_id).all()
        card_list = []
        for card in cards:
            card_list.append(card.to_dict())
        return jsonify(card_list), 200
    else:
        return jsonify("Card does not exist!"), 404

# Post a card to a board
@board_bp.route("/<board_id>/cards", methods=["POST"])
def create_card_for_board(board_id):
    board_id = int(board_id)
    board = Board.query.get(board_id)
    if board:
        form_data = request.get_json()
        new_card = Card(message=form_data["message"],
        likes_count=form_data["likes_count"],
        board_id=board_id
        )
        db.session.add(new_card)
        db.session.commit()
        return jsonify(new_card.to_dict()), 201
    else:
        return jsonify("Board does not exist!"), 404

# Delete cards
@card_bp.route("/<card_id>", methods=["DELETE"])
def delete_card(card_id):
    card_id = int(card_id)
    card = Card.query.get(card_id)

    if card:
        db.session.delete(card)
        db.session.commit()
        return jsonify("Card was succesfully deleted"), 200
    else:
        return jsonify("Card does not exist"), 404

# Update a card with likes
@card_bp.route("/<card_id>/like", methods=["PUT"])
def like_card(card_id):
    card_id = int(card_id)
    card = Card.query.get(card_id)
    if card:
        card.likes_count += 1
        db.session.commit()
        return jsonify(card.to_dict()), 200
    else:
        return jsonify("Card does not exist"), 404