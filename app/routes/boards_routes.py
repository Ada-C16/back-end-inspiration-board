from flask import Blueprint, request, jsonify, make_response
from app.helpers.boards_helpers import list_of_boards, require_valid_id
from app.routes.cards_routes import *
from app.models.board import Board
from app.models.card import Card
from app import db
from app.helpers.boards_helpers import *

# example_bp = Blueprint('example_bp', __name__)

boards_bp = Blueprint("boards", __name__, url_prefix="/boards")


# POST /boards Creates a new board.
# params: title (string), name (string)
# returns a dictionary with board data. 
@boards_bp.route("", methods=["POST"])
@require_valid_request_body
def create_new_board (request_body):

    new_board = Board()
    new_board.update_attributes(request_body)

    db.session.add(new_board)
    db.session.commit()

    return new_board.board_details(), 201



# GET /boards Gets a list of all boards.
# returns a dictionary of boards data.
# return empty array if no boards have been created.
<<<<<<< HEAD
# @boards_bp.route("", methods=["GET"])
# def 
=======
@boards_bp.route("", methods=["GET"])
def get_boards():

    boards = Board.query.all()

    return list_of_boards(boards), 200
>>>>>>> 7bc04f4b5fb0f843931978a1bf27a4b57d6dd9b5


# GET /boards/<board_id> Gets data for specific board.
# returns a dictionary of the board's data.
<<<<<<< HEAD
# @boards_bp.route("/<board_id>", methods=["GET"])

# GET /boards/<board_id>/cards Gets all cards assigned to a specific board.
# returns a dictionary of cards data for the board.
# @boards_bp.route("/<board_id>/cards", methods=["GET"])
# def
=======
@boards_bp.route("/<board_id>", methods=["GET"])
@require_valid_id
def get_one_board(board):

    return board.board_details(), 200

# GET /boards/<board_id>/cards Gets all cards assigned to a specific board.
# returns a dictionary of cards data for the board.
@boards_bp.route("/<board_id>/cards", methods=["GET"])
@require_valid_id
def cards_of_one_board(board):

    boards_cards = Card.query.filter(Card.board_id==board.board_id)

    all_cards = []

    for card in boards_cards:
        all_cards.append(card.card_details()) # May need to break this up into two separate steps. Wanted to see if this implementation worked.

    return all_cards, 200
>>>>>>> 7bc04f4b5fb0f843931978a1bf27a4b57d6dd9b5


# Enhancement ideas - DELETE, PUT/PATCH board info