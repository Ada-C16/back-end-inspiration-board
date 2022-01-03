from flask import Blueprint, json, request, jsonify, make_response
from app import db
from app.models.board import Board
from app.models.card import Card

boards_bp = Blueprint("boards", __name__, url_prefix="/boards")
cards_bp = Blueprint("cards", __name__, url_prefix="/cards")

# TODO routes/methods:
# GET /boards/<board_id>/cards
# POST /boards/<board_id>/cards
# DELETE /cards/<card_id>
# PUT /cards/card_id
# OPTIONAL: DELETE /boards/<board_id>
# OPTIONAL: PUT /boards/<board_id>

@boards_bp.route("", methods=["POST"])
def create_board():
    req = request.get_json()
    new_board = Board(
        title=req["title"],
        owner=req["owner"]
    )
    db.session.add(new_board)
    db.session.commit()
    response_body = {
        "title": new_board.title,
        "owner": new_board.owner,
        "board_id": new_board.board_id
    }
    return jsonify(response_body), 201


@boards_bp.route("", methods=["GET"])
def read_all_boards():
    boards = Board.query.all()
    
    response_body = []

    for board in boards:
        response_body.append({
            "title": board.title,
            "owner": board.owner,
            "board_id": board.board_id
        })

    return jsonify(response_body), 200

    

