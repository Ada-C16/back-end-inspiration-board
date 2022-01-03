from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.board import Board
from app.models.card import Card

# example_bp = Blueprint('example_bp', __name__)

board_bp = Blueprint("board", __name__, url_prefix="/board")

def validate_board(request_body):
    if "title" not in request_body or "owner" not in request_body:
        return jsonify({"details": "Request body must include title and author"}), 400

# Get all Boards
@board_bp.route("", methods=["GET"])
def get_all_boards():
    boards = Board.query.all()
    board_list = []
    for board in boards:
        board_list.append(board.to_dict())
    return jsonify(board_list), 200

#get single a single board
@board_bp.route("/<board_id>", methods=["GET"])
def get_single_board(board_id):
    board = Board.query.get(board_id)
    if board:
        return board.to_dict(), 200
    else:
        return jsonify({"This board does not exist, Make a board"}), 404

#post a board
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
        return jsonify("invalid data"), 404

@board_bp.route("/<board_id>", methods=["DELETE"])
def delete_board(board_id):
    board_id = int(board_id)
    board = Board.query.get(board_id)

    if board:
        db.session.delete(board)
        db.session.commit()
        return jsonify("Board was succesfully deleted"), 200
    else:
        return jsonify("board does not exist"), 404
