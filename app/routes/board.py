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

    db.session.add(new_board)
    db.session.commit()

    return jsonify(new_board.to_dict()), 201

# GET and POST for  /boards/<board_id>/cards
@bp.route("/<board_id>/cards", methods=["GET", "POST"])
def handle_cards(board_id):
    board = Board.query.get(board_id)
    if board is None:
        return "The board does not exist!", 404

    if request.method == "POST":
        request_body = request.get_json()
        if "message" not in request_body:
            abort(make_response({"error": "Card must include message!"}, 400))
        new_card = Card(
        message=request_body["message"],
        likes_count=0,
        board_id=board_id
    )
        db.session.add(new_card)
        db.session.commit()
        return jsonify({"message": f"New card is successfully created."}), 201

    elif request.method == "GET":
        cards_response = []
    for card in board.card:
        cards_response.append(card.to_dict())

    return jsonify({
        "id":board.board_id,
        "title":board.title,
        "cards" :cards_response
        })