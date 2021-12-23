from flask import Blueprint, request, jsonify, make_response
from app.routes.cards_routes import *
from app.models.board import Board
from app.models.card import Card
from app import db
from app.helpers.boards_helpers import *

boards_bp = Blueprint("boards", __name__, url_prefix="/boards")

# POST /boards Creates a new board.
# params: title (string), name (string)
# returns a dictionary with board data. 
@boards_bp.route("", methods=["POST"])
@require_valid_request_body
def create_new_board(request_body):

    new_board = Board()
    new_board.update_attributes(request_body)

    db.session.add(new_board)
    db.session.commit()

    return new_board.board_details(), 201


# GET /boards Gets a list of all boards.
# returns a dictionary of boards data.
# return empty array if no boards have been created.
@boards_bp.route("", methods=["GET"])
def get_boards():

    boards = Board.query.all()

    return list_of_boards(boards), 200


# GET /boards/<board_id> Gets data for specific board.
# POST /boards/<board_id> Creates a new card to a specific board
# returns a dictionary of the board's data.
@boards_bp.route("/<board_id>", methods=["GET", "POST"])
@require_valid_id
def one_board(board):
    if request.method == "GET":
        return board.board_details(), 200

    elif request.method == "POST":
        request_body = request.get_json()

        if request_body["message"]== "":
            return {"details": "Request body must include message."}, 400
        
        new_card = Card()
        board_id = board.board_id
        new_card.update_attributes(board_id, request_body)

        db.session.add(new_card)
        db.session.commit()

        return new_card.card_details(), 200

# GET /boards/<board_id>/cards Gets all cards assigned to a specific board.
# returns a dictionary of cards data for the board.
@boards_bp.route("/<board_id>/cards", methods=["GET"])
@require_valid_id
def cards_of_one_board(board):

    boards_cards = Card.query.filter(Card.board_id==board.board_id)

    all_cards = []

    for card in boards_cards:
        all_cards.append(card.card_details()) # May need to break this up into two separate steps. Wanted to see if this implementation worked.

    return jsonify(all_cards), 200


# Enhancement ideas - DELETE, PUT/PATCH board info