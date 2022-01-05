from flask import Blueprint, json, request, jsonify, make_response
from app import db
from app.models.board import Board
from app.models.card import Card
from datetime import datetime, timezone


boards_bp = Blueprint("boards", __name__, url_prefix="/boards")
cards_bp = Blueprint("cards", __name__, url_prefix="/cards")

# TODO routes/methods:
# OPTIONAL: DELETE /boards/<board_id>
# OPTIONAL: PUT /boards/<board_id>
# OPTIONAL: PUT (undo) (we could double up logic)

@boards_bp.route("", methods=["POST"])
def create_board():
    req = request.get_json()
    resp = Board.from_dict(req)
    if isinstance(resp, dict):
        code = 400
    else:
        code = 201
        db.session.add(resp)
        db.session.commit()
        resp = resp.to_dict()
    return jsonify(resp), code

@boards_bp.route("", methods=["GET"])
def read_all_boards():
    boards = Board.query.all()
    resp = [board.to_dict() for board in boards]
    return jsonify(resp), 200

@boards_bp.route("/<board_id>/cards", methods=["POST"])
def create_card(board_id):
    # optional enhancement: send slack message whenever a card is created
    req = request.get_json()

    board = Board.get_board(board_id)
    if not board:
        resp = {"error": "ID must be an integer"}
        code = 400
    else:
        resp = Card.from_dict(req, board_id)
        if isinstance(resp, dict):
            code = 400
        else:
            code = 201
            db.session.add(resp)
            db.session.commit()
            resp = resp.to_dict()
    return jsonify(resp), code


@boards_bp.route("/<board_id>/cards", methods=["GET"])
def read_all_cards(board_id):
    board = Board.get_board(board_id)
    if not board:
        return jsonify({"error": "ID must be an integer"}), 400
    resp = board.get_all_cards()
    return jsonify(resp), 200


@cards_bp.route("/<card_id>", methods=["DELETE"])
def delete_card(card_id):
    card = Card.get_card(card_id)
    card.delete_card()
    db.session.commit()
    return jsonify(''), 204
    
    

@cards_bp.route("/<card_id>/like", methods=["PUT"])
def update_card(card_id):
    card = Card.get_card(card_id)
    if not card.deleted_at:
        resp = card.add_like()
        db.session.commit()
        return jsonify(resp), 200
    else:
        return jsonify({"error": "You cannot like a deleted card"}), 400
    