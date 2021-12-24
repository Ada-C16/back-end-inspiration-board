from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.board import Board
from app.models.card import Card

bp = Blueprint("boards", __name__, url_prefix="/boards")

# Helper functions
def validate_request_body(request_body):
    """Validates that mandatory fields present in request body.
    Aborts with a 400 if required data missing.
    """
    mandatory_fields = ["title", "owner"]
    for field in mandatory_fields:
        if field not in request_body:
            abort(make_response({"error": f"User must include {field}."}, 400))
    return True

# GET /boards
@bp.route("", methods=["GET"])
def get_board():
    """Reads all created boards"""
    boards_response = []
    boards = Board.query.all()

    for board in boards:
        boards_response.append(board.to_dict())

    return jsonify(boards_response), 200

# POST /board
@bp.route("", methods=["POST"])
def post_board():
    """Creates a new board from user input."""
    data = request.get_json()
    validate_request_body(data)

    new_board = Board(
        title=data["title"],
        owner=data["owner"]
    )
    # TODO: Do we not need to include 'card=' here? It's blank
        # until a user adds a new one? My guess is card is blank
        # at the point of the POST request/board creation...

    db.session.add(new_board)
    db.session.commit()

    return jsonify({"message": f"Created {new_board.title} successfully."}), 201

# GET /boards/<board_id>/cards

# POST /boards/<board_id>/cards