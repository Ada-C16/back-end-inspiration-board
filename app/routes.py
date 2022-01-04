from flask import Blueprint, request, jsonify, make_response
from .models.board import Board
from .models.card import Card
from app import db
from datetime import date

board_bp = Blueprint('board', __name__, url_prefix="/board")
card_bp = Blueprint('card', __name__, url_prefix="/card")

# Adds a new board
@board_bp.route("", methods=["POST"], strict_slashes=False)
def create_new_board():
    request_body = request.get_json()
    if not Board.validate_data(request_body):
        return make_response(jsonify({"message": f"invalid data"})
    , 400)
    board_name = request_body["name"]
    new_board = Board(
        name = board_name
    )

    db.session.add(new_board)
    db.session.commit()
    return make_response(jsonify({"message": f"{board_name} board successfully created"})
    , 201)

# Gets a list of all existing boards and their ids
@board_bp.route("", methods=["GET"], strict_slashes=False)
def get_board_names():
    boards = Board.query.all()
    response = []
    for board in boards:
        response.append({
            "name":board.name,
            "id":board.id
        })
    return make_response(jsonify({"boards": response}), 200)

# Posts a new sticky to an existing board
@board_bp.route("/<board_id>", methods=["POST"], strict_slashes=False)
def add_card(board_id):
    board = Board.query.get_or_404(board_id)
    request_body = request.get_json()
    if not Card.validate_data(request_body):
        return make_response(jsonify({"message": f"invalid data"})
    , 400)
    new_card = Card(board_id=board_id, value=request_body["text"], date=date.today())
    db.session.add(new_card)
    db.session.commit()
    return make_response(jsonify({"message": f"card successfully added to {board.name} board", "text": request_body["text"]}), 201)

# Gets all cards for an existing board
@board_bp.route("/<board_id>", methods=["GET"], strict_slashes=False)
def get_cards_for_boards(board_id):
    board = Board.query.get_or_404(board_id)
    stickies = board.get_all_stickies()
    return make_response(jsonify(stickies), 200)

# Deletes an existing board
@board_bp.route("/<board_id>", methods=["Delete"], strict_slashes=False)
def delete_one_empty_board(board_id):
    board = Board.query.get_or_404(board_id)
    if len(board.cards) != 0:
        return make_response(jsonify({"message": f"{board.name} cannot be deleted until it has no stickies"})
    , 400)
    db.session.delete(board)
    db.session.commit()
    return make_response(jsonify({"message": f"{board.name} board successfully deleted"})
    , 200)

# Deletes an existing card
@board_bp.route("<board_id>/<card_id>", methods=["Delete"], strict_slashes=False)
def delete_one_card(board_id, card_id):
    card = Card.query.get_or_404(card_id)
    board = Board.query.get_or_404(board_id)
    if card.board_id != int(board_id):
        return make_response(jsonify({"message": f"Card #{card_id} not associated with {board.name} board"})
    , 400)
    db.session.delete(card)
    db.session.commit()
    return make_response(jsonify({"message": f"Card #{card_id} from {board.name} board successfully deleted"})
    , 200)

# Likes one card from an existing board
@board_bp.route("<board_id>/<card_id>", methods=["Patch"], strict_slashes=False)
def update_one_card_likes(board_id, card_id):
    card = Card.query.get_or_404(card_id)
    board = Board.query.get_or_404(board_id)
    if card.board_id != int(board_id):
        return make_response(jsonify({"message": f"Card #{card_id} not associated with {board.name} board"})
    , 400)
    card.num_likes += 1
    db.session.commit()

    return make_response(jsonify({"message": f"Card #{card_id} from {board.name} board successfully liked"})
    , 200)
