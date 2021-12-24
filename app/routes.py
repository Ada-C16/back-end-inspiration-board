from flask import Blueprint, request, jsonify
from app import db
from app.models import board
from app.models.card import Card
from app.models.board import Board


cards_bp = Blueprint("cards", __name__, url_prefix="/cards")
boards_bp = Blueprint("boards", __name__, url_prefix="/boards")


# CREATE
# Create a new board
@boards_bp.route("", methods=['POST'])
def create_board():
    request_body = request.get_json()
    if "owner" not in request_body or "title" not in request_body:
        return jsonify("Not Found"), 404

    new_board = Board(owner=request_body["owner"], title=request_body["title"])

    db.session.add(new_board)
    db.session.commit()

    return jsonify(f"{new_board.title} successfully created."), 201


# Create a new card
@cards_bp.route("/<board_id>/cards", methods=['POST'])
#front-end needs a click event to provide API call to backend with board id
def create_card(board_id):
    board = Board.query.get(board_id)
    if board is None:
        return jsonify("Not Found"), 404

    request_body = request.get_json()

    if "message" not in request_body:
        return jsonify("Not Found"), 404

    new_card = Card(board_id = board.id, message=request_body["message"], likes_count=0)

    db.session.add(new_card)
    db.session.commit()

    return jsonify(f"Card number {new_card.card_id} successfully created."), 201



# READ
# All cards within a board
@boards_bp.route("/<board_id>/cards", methods=['GET'])
def retrieve_cards(board_id):
    board = Board.query.get(board_id)
    if board is None:
        return jsonify("Not Found"), 404
        
    cards_response = [card.card_dict() for card in board.cards]

    return jsonify(cards_response), 200


@boards_bp.route("", methods=["GET"])
def retrieve_boards():
    boards = Board.query.all()
    boards_response = [board.board_dict() for board in boards]
    
    return jsonify(boards_response), 200


# UPDATE
# Can update cards by adding 'likes'
@cards_bp.route("/<card_id>", methods=["PATCH"])
def update_card(card_id):
    card = Card.query.get(card_id)
    if card is None:
        return jsonify("Not Found"), 404

    card.likes_count += 1

    db.session.commit()

    return jsonify(f"Card {card.card_id} successfully updated. Current likes count = {card.likes_count}"), 200


# DELETE
# Can delete a single board
@boards_bp.route("/<board_id>", methods=["DELETE"])
def delete_board(board_id):
    board = Board.query.get(board_id) 

    for card in board.cards:
        db.session.delete(card)
    db.session.delete(board)
    db.session.commit()

    return jsonify(f"Board {board.id} successfully deleted.")


# Can delete cards in a board
@cards_bp.route("/<card_id>", methods=["DELETE"])
def delete_card(card_id):
    card = Card.query.get(card_id) 

    db.session.delete(card)
    db.session.commit()

    return jsonify(f"Card {card.card_id} successfully deleted.")



