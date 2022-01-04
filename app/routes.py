from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.board import Board
from app.models.card import Card

# example_bp = Blueprint('example_bp', __name__)
board_bp = Blueprint('board_bp', __name__, url_prefix="/boards")

#validate data helper function
def validate_data(request_body, required_attributes):
    for attribute in required_attributes:
        if attribute not in request_body:
            abort(make_response(jsonify({"details": f"Request body must include {attribute}."}), 400))
    return request_body

@board_bp.route("", methods=["GET", "POST"])
def handle_boards():
    if request.method == "GET":
        boards = Board.query.all()  # list of board objects
        boards_response = []
        for board in boards:
            boards_response.append({
                "board_id": board.board_id,
                "title": board.title,
                "owner": board.owner
            })

        return make_response(jsonify(boards_response), 200)

    elif request.method == "POST":
        required_attributes = ["title", "owner"]
        request_body = validate_data(request.get_json(), required_attributes)
        new_board = Board(title = request_body["title"],owner = request_body["owner"])

        db.session.add(new_board)
        db.session.commit()

        return make_response(new_board.to_json()), 201

@board_bp.route("/<board_id>/cards", methods=["GET", "POST"])
def handle_board_card(board_id):
    if request.method == "GET":
        
        cards = Card.query.filter(Card.board_id == board_id)

        return jsonify([card.to_json() for card in cards]), 200

    if request.method == "POST":
        
        request_body = request.get_json()

        new_card = Card(message=request_body["message"], board_id=board_id)

        db.session.add(new_card)
        db.session.commit()

        return make_response(new_card.to_json(), 201)


# Some notes about routes
#   - DELETE /cards/card_id
#     - Delete the selected card
#   - PATCH /cards/card_id
#       - Like card
