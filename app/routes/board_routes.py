from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.board import Board
from app.models.card import Card

import app.validate as validate

boards_bp = Blueprint("boards", __name__, url_prefix="/boards")


@boards_bp.route("", methods=["POST"])
def create_board():

    request_body = request.get_json()

    try:
        new_board = Board(
            title=request_body["title"],
            owner=request_body["owner"],
        )
        db.session.add(new_board)
        db.session.commit()

        return new_board.to_dict(), 201

    except KeyError:

        return make_response(validate.missing_fields(request_body, Board), 400)


@boards_bp.route("", methods=["GET"])
def get_boards():

    boards = Board.query.all()
    return jsonify([board.to_dict() for board in boards])


@boards_bp.route("/<id>", methods=["GET"])
def get_board(id):
    board_id = validate.valid_id(id)
    board = validate.valid_model(board_id, Board)

    return board.to_dict()


@boards_bp.route("/<id>/cards", methods=["GET"])
def get_card_by_board_id(id):

    board_id = validate.valid_id(id)
    board = validate.valid_model(board_id, Board)
    cards = Card.query.filter_by(board_id=board_id).all()

    return jsonify([card.to_dict() for card in cards])

@boards_bp.route("/<id>/cards", methods=["POST"])
def create_card(id):

    board_id = validate.valid_id(id)
    request_body = request.get_json()

    try:
        new_card = Card(
            message=request_body["message"],
            likes_count=request_body["likes_count"],
            board_id=board_id,
        )
        db.session.add(new_card)
        db.session.commit()

        return new_card.to_dict(), 201

    except KeyError:

        return make_response(validate.missing_fields(request_body, Card), 400)


@boards_bp.route("/<id>", methods=["DELETE"])
def delete_board(id):
    board_id = validate.valid_id(id)
    board = validate.valid_model(board_id, Board)

    db.session.delete(board)
    db.session.commit()
    response_body = {"details": f"Board {board.id} {board.title} successfully deleted"}
    return make_response(response_body), 200
