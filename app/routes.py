from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.board import Board
from app.models.card import Card
from .helper_functions import *

board_bp = Blueprint("boards", __name__, url_prefix="/boards")
card_bp = Blueprint("cards", __name__, url_prefix="/cards")

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
    
    return {"New board created with id": new_board.board_id}, 201

@board_bp.route("", methods = ["DELETE"])
def delete_all_boards_but_default():
    """Deletes all boards and cards associated with boards from database, 
    except for th@e default board."""
    boards = Board.query.filter(Board.board_id!=1).all()
    
    for board in boards: 
        if board.cards:
            for card in board.cards: 
                delete_from_database(card)

        delete_from_database(board)

    return {"All boards but one were deleted."}, 200

####---------------------------------------------------####
####------------------ CARD ENDPOINTS -----------------####
####---------------------------------------------------####

# ---3----
# Route: "/cards/<card_id>"
# Method: PUT
# 1. Data check -> 
#       - is it numeric? make_response({"message" : "Please enter a valid board id"}, 400)
#       - does card_id exist? make_response({"message" : f"{entity} {id} was not found"}, 404)
# 2. database query by card_id
        # - card=Card.query.get(card_id)
        # - card.like_count +=1
# 3. make_response("Successfully updated like count", 200)

# ---4----
# Route: "/cards/<card_id>"
# Method: DELETE
# 1. Data check -> 
#       - is it numeric? make_response({"message" : "Please enter a valid board id"}, 400)
#       - does board_id exist? make_response({"message" : f"{entity} {id} was not found"}, 404)
# 2. database query by card_id
        # - Card.query(card_id)
# 3. db.session.delete(card)
# 4. db.session.commit()
# 5. make_response("Successfully deleted card", 200)

# ---5----
# Route: "/cards/<card_id>"
# Method: POST
# 1. request_body = request.get_json()
# 2. check request data - make sure message is present
# 3. create new card 
        # - new_card = Card(message=request_body["message"])
# 4. db.session.add(new_card)
# 5. db.session.commit()
# 4. return ....what to return here?? dict of new card? + 200 OK?



