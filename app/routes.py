from flask import Blueprint, request, jsonify
from app import db
from app.models.board import Board
from app.models.card import Card
import os
import requests


boards_bp = Blueprint("boards", __name__, url_prefix="/boards")
cards_bp = Blueprint("cards", __name__, url_prefix="/cards")

# TODO routes/methods:
# OPTIONAL: DELETE /boards/<board_id>
# OPTIONAL: PUT /boards/<board_id>
# OPTIONAL: PUT (undo) (we could double up logic)

# LUX WAS HERE!
@cards_bp.errorhandler(400)
@boards_bp.errorhandler(400)
def handle_invalid_data(error):
    resp = jsonify({"error": error.description}), 400
    return resp


@boards_bp.route("", methods=["POST"])
def create_board():
    req = request.get_json()
    board = Board.from_dict(req)
    db.session.add(board)
    db.session.commit()
    return jsonify(board.to_dict()), 201


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
    card = Card.from_dict(req, board_id)

    db.session.add(card)
    db.session.commit()

    SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
    SLACK_CHANNEL_ID = os.environ.get("SLACK_CHANNEL_ID")
    path = "https://slack.com/api/chat.postMessage"
    headers = {"Authorization": f"Bearer {SLACK_BOT_TOKEN}"}

    req_body = {
        "channel": SLACK_CHANNEL_ID,
        "text": f"Someone just posted a card to the board {board.title} saying: {card.message}",
    }

    requests.post(path, headers=headers, data=req_body)

    return jsonify(card.to_dict()), 201


@boards_bp.route("/<board_id>/cards", methods=["GET"])
def read_all_cards(board_id):
    board = Board.get_board(board_id)
    resp = board.get_all_cards()
    return jsonify(resp), 200


@cards_bp.route("/<card_id>", methods=["DELETE"])
def delete_card(card_id):
    card = Card.get_card(card_id)
    card.delete_card()
    db.session.commit()
    return jsonify(""), 204


@cards_bp.route("/<card_id>/like", methods=["PUT"])
def update_card(card_id):
    card = Card.get_card(card_id)
    card = card.add_like()
    db.session.commit()
    return jsonify(card.to_dict()), 200
