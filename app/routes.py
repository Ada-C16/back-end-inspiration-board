from flask import Blueprint, json, request, jsonify, make_response
from app import db
from app.models.board import Board
from app.models.card import Card
from datetime import datetime, timezone


boards_bp = Blueprint("boards", __name__, url_prefix="/boards")
cards_bp = Blueprint("cards", __name__, url_prefix="/cards")

# TODO routes/methods:
# DELETE /cards/<card_id>
# PUT /cards/card_id
# OPTIONAL: DELETE /boards/<board_id>
# OPTIONAL: PUT /boards/<board_id>
# OPTIONAL: PUT (undo) (we could double up logic)

@boards_bp.route("", methods=["POST"])
def create_board():
    req = request.get_json()
    new_board = Board(
        title=req["title"],
        owner=req["owner"]
    )
    db.session.add(new_board)
    db.session.commit()
    resp = {
        "title": new_board.title,
        "owner": new_board.owner,
        "board_id": new_board.board_id
    }
    return jsonify(resp), 201


@boards_bp.route("", methods=["GET"])
def read_all_boards():
    boards = Board.query.all()
    
    resp = []

    for board in boards:
        resp.append({
            "title": board.title,
            "owner": board.owner,
            "board_id": board.board_id
        })

    return jsonify(resp), 200

@boards_bp.route("/<board_id>/cards", methods=["POST"])
def create_card(board_id):
    # optional enhancement: send slack message whenever a card is created
    req = request.get_json()

    new_card = Card(
        message=req["message"],
        board_id=board_id
    )

    db.session.add(new_card)
    db.session.commit()
    
    resp = {
        "message": new_card.message,
        "card_id": new_card.card_id,
        "likes_count": new_card.likes_count
    }

    return jsonify(resp), 201


@boards_bp.route("/<board_id>/cards", methods=["GET"])
def read_all_cards(board_id):
    board = Board.query.get_or_404(board_id)
    resp = []
    for card in board.cards:
        if not card.deleted_at:
            resp.append({
                "card_id": card.card_id,
                "message": card.message,
                "likes_count": card.likes_count
            })
    return jsonify(resp), 200


@cards_bp.route("/<card_id>", methods=["DELETE"])
def delete_card(card_id):
    card = Card.query.get_or_404(card_id)

    card.deleted_at = datetime.now(timezone.utc)

    db.session.commit()

    return 204
    
    



# TODO: consider a patch request with an endpoint like /<card_id>/like to update likes instead
@cards_bp.route("/<card_id>", methods=["PUT"])
def update_card(card_id):
    card = Card.query.get_or_404(card_id)
    req = request.get_json()
    card.likes_count = req["likes_count"]
    # TODO THIS ROUTE

    db.session.commit()
    resp = {
        "messages": card.messages,
        "likes_count": card.likes_count
    }

    return jsonify(resp), 200
    