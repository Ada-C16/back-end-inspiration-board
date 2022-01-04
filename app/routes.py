from flask import Blueprint, request, jsonify, make_response
from flask.globals import request 
from app.models.board import Board, to_dict 
from app.models.card import Card 
from app import db

# example_bp = Blueprint('example_bp', __name__)

########## BOARD ROUTES ##########
board_bp = Blueprint("board_bp", __name__, url_prefix="/board")

@board_bp.route("", methods=["POST"])
def create_board():
    request_body = request.get_json()
    
    missing = ""
    if "title" not in request_body:
        missing = "title"
    elif "owner" not in request_body:
        missing = "owner"
    if missing:
        return{"details": f"Request body must include {missing}."}, 400

    new_board = Board(
        title=request_body["title"],
        owner=request_body["owner"]
    )

    db.session.add(new_board)
    db.session.commit()

    return {"id": new_board.board_id}, 201

@board_bp.route("", methods=["GET"])
def read_boards():
    boards = Board.query.all()

    response_body = []

    if not boards:
        return jsonify([]), 200

    for board in boards:
        response_body.append(board.to_dict())

    return jsonify(response_body), 200

@board_bp.route("/<id>", methods=["PUT", "PATCH"])  #woudl it be board_id???
def update_board(board_id):
    request_body = request.get_json()

    board = Board.query.get(board_id)

    if not board:
        return {"message": f"Board {board_id} was not found"}, 404 

    if "title" not in request_body or "owner" not in request_body:
        return {"details":  "Invalid request"}, 400 

    board.title =



########## CARD ROUTES ##########
card_bp = Blueprint("card_bp", __name__, url_prefix="/card")


