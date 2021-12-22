from flask import Blueprint, json, jsonify, request

from app import db
from app.models.board import Board
from app.models.card import Card

boards_bp = Blueprint("boards_bp", __name__, url_prefix="/boards")

@boards_bp.route("", methods=["GET"])
def get_boards():
    boards = Board.query.all()
    if boards == None:
        return jsonify("No boards found", 404)
    else:
        response_body = []
        for board in boards:
            response_body.append(board.response_dict())

    return jsonify(response_body), 200

@boards_bp.route("", methods=["POST"])
def post_board():
    request_body = request.get_json()
    if "title" not in request_body:
        response_body = {"details": "Request body must include name."}
        return jsonify(response_body), 400
    elif "owner" not in request_body:
        response_body = {"details": "Request body must include postal_code."}
        return jsonify(response_body), 400

    new_board = Board(
        title = request_body["title"],
        owner = request_body["owner"]
    )
    db.session.add(new_board)
    db.session.commit()
    response_body = new_board.response_dict()
    return jsonify(response_body), 201

@boards_bp.route("/<board_id>", methods=["GET"])
def get_videos_by_id(board_id):
    if not board_id.isnumeric():
        return jsonify(None), 400
    board = Board.query.get(board_id)
    if not board:
        return jsonify({"message": f"{board_id} was not found"}), 404

    response_body = board.response_dict()

    return jsonify(response_body), 200

@boards_bp.route("/<board_id>/cards", methods=["GET"])
def get_cards_by_board(board_id):
    if not board_id.isnumeric():
        return jsonify(None), 400
    board = Board.query.get(board_id)
    if not board:
        return jsonify({"message": f"{board_id} was not found"}), 404

    card_response = [card.id for card in board.cards]

    response_body = []
        # [Card.query.get(card).create_dict() for card in card_response] <= update when I have the name of the card method

    return jsonify(response_body), 200

# POST /boards/<board_id>/cards
boards_bp.route("/<board_id>/cards", methods=["POST"])
def get_cards_by_board(board_id):
    if not board_id.isnumeric():
        return jsonify(None), 400
    board = Board.query.get(board_id)
    if not board:
        return jsonify({"message": f"{board_id} was not found"}), 404

    request_body = request.get_json()

    if "message" not in request_body:
        response_body = {"details": "Request body must include message."}
        return jsonify(response_body), 400
    
    new_card = Card(
        board_id=request_body["board_id"],
        message=request_body["message"],
        likes_count = 0,
    )
    db.session.add(new_card)
    db.session.commit()
    # response_body = new_card.rental_dict() <= update when I have the name of the card method
    return jsonify(response_body), 200
