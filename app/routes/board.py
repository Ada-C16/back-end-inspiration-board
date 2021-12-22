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

@boards_bp.route("/<board_id>", methods=["GET"])
def get_videos_by_id(board_id):
    if not board_id.isnumeric():
        return jsonify(None), 400
    board = Board.query.get(board_id)
    if not board:
        return jsonify({"message": f"{board_id} was not found"}), 404
    # if board.deleted_at:
    #     return jsonify(None), 404
    response_body = board.response_dict()

    return jsonify(response_body), 200
