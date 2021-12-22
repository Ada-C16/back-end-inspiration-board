from app import db
from app.models.board import Board
from flask import Blueprint, request, jsonify


boards_bp = Blueprint("boards", __name__, url_prefix="/boards")

@boards_bp.route("", methods=["GET"])
def handle_boards():
    all_boards = Board.query.all()
    board_titles = [board.title for board in all_boards]
    return jsonify(board_titles), 200

@boards_bp.route("", methods=["POST"])
def post_board():
    request_body = request.get_json()
    try:
        new_board = Board(title = request_body["title"], owner = request_body["owner"])
    except:
        return jsonify("unsuccessful post"), 400
    db.session.add(new_board)
    db.session.commit()
    return jsonify("successful post"), 201

@boards_bp.route("/<id>", methods=["GET"])
def get_board_cards(id):
    board = Board.query.get(id)
    if board is None:
        return jsonify(""), 404
    cards = []

    for card in board.cards:
        cards.append({
            "id": card.card_id,
            "message": card.message,
            "likes_count": card.likes_count
        })
    board_info = {
        "title": board.title,
        "owner": board.owner,
        "cards": cards
    }
    return jsonify(board_info), 200

@boards_bp.route("/<id>", methods=["DELETE"])
def delete_board(id):
    board = Board.query.get(id)
    if board is None:
        return jsonify(""), 404
    db.session.delete(board)
    db.session.commit()
    return jsonify(f"successfully deleted {board.title}"), 200