from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.board import Board
from app.models.card import Card

# example_bp = Blueprint('example_bp', __name__)

cards_bp = Blueprint("cards", __name__, url_prefix="/cards")
boards_bp = Blueprint("boards", __name__, url_prefix="/boards")

@boards_bp.route("", methods=["GET", "POST"])
def handle_boards():
    if request.method == "POST":
        request_body = request.get_json()
        if "title" not in request_body or  request_body["title"] == "":
            return jsonify(details="Invalid request, a title is required."), 400
        if "owner" not in request_body or request_body["owner"] == "":
            return jsonify(details="Invalid request, an owner is required."), 400
        new_board = Board(title=request_body["title"],
                    owner=request_body["owner"])

        db.session.add(new_board)
        db.session.commit()

        return make_response(f"Board {new_board.title} successfully created", 201)

    if request.method == "GET":
        # title_query = request.args.get("title")
        boards = Board.query.all()
        boards_response = []
        for board in boards:
            boards_response.append({
                "id" : board.id,
                "title" : board.title,
                "owner" : board.owner
            })
        return jsonify(boards_response), 200

# Create route for when user selects a specific board to work on 
# for likes count, will need to have an API for put to update likes

@boards_bp.route("/<id>/cards", methods=["GET", "POST", "DELETE"])
def handle_board_cards():
    if request.method == "POST":
        request_body = request.get_json()
        new_card = Card(message=request_body["message"])

        db.session.add(new_card)
        db.session.commit()

        return make_response(f"A new card was successfully created for ", 201)

# How do we connect to the board the card was created under 
# test if automatically generates through postman 
# if not try:
# new_card.board_id = id 
