from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.board import Board
from app.models.card import Card
from .helper_functions import get_id

board_bp = Blueprint("board", __name__, url_prefix="/boards")


# Create a new board, by filling out a form. The form includes "title" and "owner" name of the board.

# See an error message if I try to make a new board with an empty/blank/invalid/missing "title" or "owner" input.

# All error messages can look like a new section on the screen, a red outline around the input field, and/or disabling the input, as long as it's visible
#HELPER FUNCTIONS

# def valid_int(number, parameter_type):
#     try:
#         number = int(number)
#     except:
#         abort(400, {"error": f"{parameter_type} must be an int"})


#BOARD ROUTES
# CREATE BOARD
@board_bp.route("", methods=["POST"])
def create_board():
    request_body = request.get_json()
    if not request_body.get("title"):
        abort(400, {"details":"Missing title."})
    elif not request_body.get("owner"):
        abort(400, {"details":"Missing owner_name."})
    new_board = Board(
        title=request_body["title"],
        owner=request_body["owner"],
    )

    db.session.add(new_board)
    db.session.commit()

    return make_response(f"Board {new_board.id} created!"), 201

# READ ALL BOARDS
@board_bp.route("", methods=["GET"])
def read_all_boards():
    boards = Board.query.all()
    boards_response = []
    for board in boards:
        boards_response.append(
            board.to_dict()
        )

    return jsonify(boards_response)

# READ ONE BOARD
@board_bp.route("<board_id>/cards", methods=["GET"])
def read_board(board_id):
    board = get_id(board_id, Board)
    response_body = board.read_cards()
    return jsonify(response_body), 200


#CARD ROUTES

@board_bp.route("/<board_id>/cards", methods=["POST"])
def create_card(board_id):
# board id -> get from React (selectBoard)
    board = get_id(board_id, Board)
    request_body = request.get_json()
    new_card = Card(
        message=request_body["message"],
        board_id=board.id, 
    )
    db.session.add(new_card)
    db.session.commit()

    response_body = {
        "message":  f"Success! Card {new_card.id} created. Yassss, you go Glen Coco!",
        "response_body": new_card.to_dict()
    }

    return jsonify(response_body), 201
    

