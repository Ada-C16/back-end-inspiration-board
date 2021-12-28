from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.card import Card
from app.models.board import Board

# example_bp = Blueprint('example_bp', __name__)
boards_bp = Blueprint ("boards", __name__, url_prefix=("/boards"))
cards_bp = Blueprint ("cards", __name__, url_prefix=("/cards"))

#CARDS
#read - GET
@cards_bp.route("", methods=["GET"])
def get_cards():
    cards = Card.query.all()

    response = []
    for card in cards:
        response.append(card.to_dict())

    return jsonify(response), 200

#create - POST
@cards_bp.route("", methods=["POST"])
def create_card():
    request_body = request.get_json()
    try:
        new_card = Card.from_dict(request_body)
        db.session.add(new_card)
        db.session.commit()

        return jsonify(new_card.to_dict()), 201
    except:
        response = {
            "details" : "Invalid request body"
        }

        return jsonify(response), 400

#read - GET (1)
@cards_bp.route("/<card_id>", methods=["GET"])
def get_card(card_id):
    if not card_id.isnumeric():
        return jsonify(None), 400

    card = Card.query.get(card_id)

    if not card:
        return jsonify({'message' : f'Card {card_id} was not found'}), 404

    return jsonify(card.to_dict()), 200
#delete - DELETE
@cards_bp.route("/<card_id>", methods=["DELETE"])
def delete_card(card_id):
    card = Card.query.get(card_id)

    if not card:
        return jsonify({'message' : f'Card {card_id} was not found'}), 404
    
    db.session.delete(card)
    db.session.commit()
    return jsonify({
        'id': card.card_id,
        'details': f'Card {card.card_id} succesfully deleted'
    }), 200



#BOARDS

#read - GET
@boards_bp.route("", methods=["GET"])
def get_boards():
    boards = Board.query.all()

    response = []
    for board in boards:
        response.append(board.to_dict())

    return jsonify(response), 200
#create - POST
@boards_bp.route("", methods=["POST"])
def post_board():
    request_body = request.get_json()
    try:
        new_board = Board.from_dict(request_body)
        db.session.add(new_board)
        db.session.commit()

        return jsonify(new_board.to_()), 201
    except:
        response = {
            "details" : "Invalid request body"
        }

        return jsonify(response), 400

#read (1) - GET
@boards_bp.route("/<board_id>", methods=["GET"])
def get_board(board_id):
    if not board_id.isnumeric():
        return jsonify(None), 400

    board = Board.query.get(board_id)

    if not board:
        return jsonify({'message' : f'Card {board_id} was not found'}), 404

    return jsonify(board.board_dict()), 200
#delete (1) - DELETE
@boards_bp.route("/<board_id>", methods=["DELETE"])
def delete_board(board_id):
    board = Board.query.get(board_id)

    if not board:
        return jsonify({'message' : f'Board {board_id} was not found'}), 404
    
    db.session.delete(board)
    db.session.commit()
    return jsonify({
        'id': board.board_id,
        'details': f'Board {board.board_id} succesfully deleted'
    }), 200