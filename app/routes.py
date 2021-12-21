from flask import Blueprint, json, request, jsonify, make_response
from app import db
from functools import wraps
from app.models.board import Board
from app.models.card import Card

# example_bp = Blueprint('example_bp', __name__)
boards_bp = Blueprint("board", __name__, url_prefix="/boards")
cards_bp = Blueprint("cards", __name__, url_prefix="/cards")

def require_board(endpoint):
    @wraps(endpoint)
    def fn(*args, board_id, **kwargs):
        board = Board.query.get(board_id)

        if not board:
            return jsonify(None), 404
        
        return endpoint(*args, board=board, **kwargs)
    return fn

def require_card(endpoint):
    @wraps(endpoint)
    def fgn(*args, card_id, **kwargs):
        card = Card.query.get(card_id)

        if not card:
            return jsonify(None), 404
        
        return endpoint(*args, card=card, **kwargs)
    return fgn

@boards_bp.route("/<board_id>/cards", methods=["POST"])
@require_board
def post_card_in_board(board):
    request_body = request.get_json()

    all_cards = []
    for card_id in request_body["card_ids"]:
        all_cards.append(Card.query.get(card_id))
    
    board.cards = all_cards

    db.session.commit()

    new_response = {
        "id": board.id,
        "card_ids" : request_body["card_ids"]
    }
    return jsonify(new_response), 200

@boards_bp.route("", methods=["POST"])
def post_board():
    request_body = request.get_json()
    new_board = Board.from_dict(request_body)

    if "title" not in request_body or "owner" not in request_body:
        return ({
        "details": "Missing information"
    }), 400

    db.session.add(new_board)
    db.session.commit()

    return jsonify({"board": new_board.to_dict()}), 201

#post likes? post cards or patch?
@cards_bp.route("", methods=["POST"])
def post_card():
    request_body = request.get_json()

    new_card = Card.from_dict(request_body)

    if "message" not in request_body:
        return ({
        "details": "Needs message"
    }), 400

    db.session.add(new_card)
    db.session.commit()

    return jsonify({"card": new_card.to_dict()}), 201

@cards_bp.route("", methods=["PATCH"])
@require_card
def patch_card(card):
    request.get_json()

    card.likes_count +=1
    
    db.session.commit()

    return jsonify({"likes_count": card.likes_count}), 200

@boards_bp.route("", methods=["GET"])
def get_all_boards():
    boards = Board.query.all()
    boards_response = [board.to_dict() for board in boards]
    return jsonify(boards_response, 200)

@cards_bp.route("", methods=["GET"])
def get_all_cards():
    cards = Card.query.all()
    cards_response = [card.to_dict() for card in cards]
    return jsonify(cards_response), 200

@boards_bp.route("<board_id>", methods=["GET"])
@require_board
def get_boards(board):
    return jsonify({"board": board.to_dict()}), 200

@cards_bp.route("<card_id>", methods=["GET"])
@require_card
def get_cards(card):
    if card.board_id:
        return jsonify({"card": card.card_to_dict_w_goal()}), 200
    return jsonify({"card": card.to_dict()})

@boards_bp.route("/<board_id>/cards", methods=["GET"])
@require_board
def get_cards_in_board(board):
    return jsonify(board.board_w_cards_to_dict()), 200

@cards_bp.route("/<card_id>", methods=["DELETE"])
@require_card
def delete_card (card):
    db.session.delete(card)
    db.session.commit()
    return jsonify({"details": (f"{card.message}) was deleted")}), 200

@boards_bp.route("/<board_id>", methods=["DELETE"])
@require_board
def delete_board(board):
    db.session.delete(board)
    db.session.commit()
    return jsonify({"details": (f"{board.title}) was deleted")}), 200