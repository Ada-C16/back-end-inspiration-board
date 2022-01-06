from flask import Blueprint, request, jsonify
from app import db
from app.models.board import Board
from app.models.card import Card
from .helper_functions import *

board_bp = Blueprint("boards", __name__, url_prefix="/boards")

####---------------------------------------------------####
####----------------- BOARD ENDPOINTS -----------------####
####---------------------------------------------------####

@board_bp.route("", methods = ["GET"])
def get_boards(): 
    """Returns list of dictionaires with board information"""
    boards = Board.query.all()
    boards_response = [board.to_dict() for board in boards]

    return jsonify(boards_response), 200

@board_bp.route("/<board_id>", methods = ["GET"])
def get_cards_from_one_board(board_id):
    """Input: ID of board. 
    Returns list of dictionaries with card info for
    cards associated with this board or
    404 if it doesn't exist."""
    board = valid_id(Board, board_id)
    cards = board.cards
    cards_response = [card.to_dict() for card in cards]

    return jsonify(cards_response), 200

@board_bp.route("", methods = ["POST"])
def create_new_board():
    """Adds new board to db and returns new board ID and 201 code or
    400 error if request body is missing title or owner."""
    request_body = request.get_json()

    valid_input(request_body, Board)

    new_board = Board(title = request_body["title"],
                    owner = request_body["owner"])

    add_to_database(new_board)
    
    return {"id": new_board.board_id}, 201

@board_bp.route("", methods = ["DELETE"])
def delete_all_boards_but_default():
    """Deletes all boards and cards associated with boards from database, 
    except for the default board."""
    boards = Board.query.filter(Board.board_id!=2).all()
    
    for board in boards: 
        if board.cards:
            for card in board.cards: 
                delete_from_database(card)

        delete_from_database(board)

    return {"id": 2}, 200

####---------------------------------------------------####
####------------------ CARD ENDPOINTS -----------------####
####---------------------------------------------------####
@board_bp.route("/<board_id>/<card_id>", methods=["PUT"])
def update_card_likes(board_id, card_id):
    """Input: Board ID and Card ID
    Updates card in database and returns success message with card ID.
    Returns 400 if invalid ID or 404 if card or board don't exist."""
    card = valid_id(Card, card_id)
    board = valid_id(Board, board_id)

    card.likes_count += 1
    db.session.commit()
    
    return {"likes_count": card.likes_count}, 200

@board_bp.route("/<board_id>/<card_id>", methods=["DELETE"])
def delete_card(board_id, card_id):
    """Input: Board ID and Card ID
    Deletes card from database and returns success message.
    Returns 400 if ID isn't valid or 404 if card or board don't exist.
    """
    card = valid_id(Card, card_id)
    board = valid_id(Board, board_id)

    delete_from_database(card)

    return {"id": card.card_id}, 200

@board_bp.route("/<board_id>/cards", methods = ["POST"])
def create_new_card(board_id):
    """Input: Board ID
    Adds card to database and returns card ID with success message.
    Returns 400 if invalid ID or 404 if board doesn't exist."""
    request_body = request.get_json()
    valid_id(Board, board_id)
    valid_input(request_body, Card)

    new_card = Card(message = request_body["message"],
                    likes_count = 0,
                    board_id = board_id)

    add_to_database(new_card)
    
    return {"id": new_card.card_id}, 201


