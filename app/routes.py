from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.board import Board

# example_bp = Blueprint('example_bp', __name__)
board_bp = Blueprint('board_bp', __name__, url_prefix="/boards")

@board_bp.route("", methods=["GET"])
def get_all_boards():
    if request.method == "GET":
        boards = Board.query.all()
        boards_response = []
        for board in boards:
            boards_response.append({
                "board_id": board.board_id,
                "title": board.title,
                "owner": board.owner
            })

        return make_response(jsonify(boards_response), 200)
    elif request.method == "POST":
        request_body = request.get_json()
        new_board = Board(title = request_body["title"],owner = request_body["owner"])

        db.session.add(new_board)
        db.session.commit()

        return make_response(jsonify({
                "board_id": new_board.board_id,
                "title": new_board.title,
                "owner": new_board.owner
            }), 201)



