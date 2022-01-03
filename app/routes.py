from flask import Blueprint, request, jsonify, make_response
from app import db

# example_bp = Blueprint('example_bp', __name__)

board_bp = Blueprint("board", __name__, url_prefix="/board")

def validate_board(request_body):
    if "title" not in request_body or "owner" not in request_body:
        return jsonify({"details": "Request body must include title and author"}), 400

@board_bp.route("", methods=["GET"])

def get_all_boards():
    board = Board.query.all()
    board_list = []
    for board in boards:
        board_list.append(board.to_dict())
    return jsonify(board_list), 200

