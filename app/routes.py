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

# TODO errorhandling ->  invalid keys in req body, invalid id for board
# TODO encapsulation -> from_json classmethod for card, to_dict instance method
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


# TODO errorhandling -> invalid board id
# TODO encapsulation -> board method using a list comprehension for getting all cards, that list comprehension will use card's to_dict method
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


# TODO errorhandling -> invalid card id (either already deleted or nonexistent)
# TODO encapsulation -> card method to delete
@cards_bp.route("/<card_id>", methods=["DELETE"])
def delete_card(card_id):
    card = Card.query.get_or_404(card_id)

    card.deleted_at = datetime.now(timezone.utc)

    db.session.commit()

    return jsonify(''), 204
    
    

# TODO errorhandling -> invalid card_id (deleted or nonexistent) 
# TODO encapsulation -> card.like() method and use to_dict for resp
@cards_bp.route("/<card_id>/like", methods=["PUT"])
def update_card(card_id):
    card = Card.query.get_or_404(card_id)
    if not card.deleted_at:
        card.likes_count += 1 

        db.session.commit()
        resp = {
            "card_id": card.card_id,
            "message": card.message,
            "likes_count": card.likes_count
        }

        return jsonify(resp), 200
    