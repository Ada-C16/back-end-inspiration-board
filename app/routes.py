from flask import Blueprint, request, jsonify, make_response
from app.models.card import Card
from app import db
from app.models.board import Board


boards_bp = Blueprint("boards_bp", __name__, url_prefix="/boards")
cards_bp = Blueprint("cards", __name__, url_prefix="/cards")

# BOARD ROUTES
@boards_bp.route("", methods=["POST", "GET"])
def handle_boards():
    # POST REQUEST
    if request.method == "POST":
        board_request_body = request.get_json()

        new_board = Board(
            owner_name=board_request_body["owner_name"],
            title=board_request_body["title"],
        )

        db.session.add(new_board)
        db.session.commit()

        new_board_response = new_board.get_board_response()

        return jsonify(new_board_response), 201

    # GET REQUEST
    elif request.method == "GET":
        board_title_query = request.args.get("title")
        board_name_query = request.args.get("owner_name")
        if board_title_query or board_name_query:
            boards = Board.query.filter(Board.title.contains(board_title_query))
            boards = Board.query.filter(Board.owner_name.contains(board_name_query))
        else:
            boards = Board.query.all()

        board_response = [board.get_board_response() for board in boards]

        if board_response == []:
            return jsonify(board_response), 200

        return jsonify(board_response), 200

# GET, PUT, DELETE ONE BOARD AT A TIME
@boards_bp.route("/<board_id>", methods=["GET", "PUT", "DELETE"])
def handle_one_board(board_id):
    if not board_id.isnumeric():
        return jsonify(None), 400

    board = Board.query.get(board_id)

    if board is None: 
        return jsonify({"Message": f"Board {board_id} was not found"}), 404
    
    if request.method == "GET":
        return jsonify(board.get_board_response()), 200

    elif request.method == "PUT":
        board_update_request_body = request.get_json()

        if "owner_name" not in board_update_request_body or "title" not in board_update_request_body:
            return jsonify(None), 400

        board.owner_name=board_update_request_body["owner_name"],
        board.title=board_update_request_body["title"]

        db.session.commit()

        updated_board_response = board.get_board_response()

        return jsonify(updated_board_response), 200
    
    elif request.method == "DELETE":

        db.session.delete(board)
        db.session.commit()

        board_delete_response = board.get_board_response()

        return jsonify(board_delete_response), 200

# Get all cards by board id (some FE event handler should use this)
@boards_bp.route("/<board_id>/cards", methods=["GET"]) 
def cards_by_board(board_id):
    cards = Card.query.filter_by(board_id=board_id)
    cards_response = [card.to_json() for card in cards]
    return jsonify(cards_response), 200

# Add a card to a particular board (some FE event handler should use this)
@boards_bp.route("/<board_id>/cards", methods=["POST"])
def add_card(board_id):
    request_data = request.get_json()
    if len(request_data['message']) > 40 or len(request_data['message']) == 0: 
        return make_response("Your message must be between 1 and 40 characters.", 400) 

    card = Card(
        message = request_data['message'],
        likes_count = 0,
        board_id = board_id
    )
    db.session.add(card)
    db.session.commit()

    return card.to_json(), 200

# CARD ROUTES

# Get all cards
# Note: this is only for testing purposes in Postman; the FE will never call it.
@cards_bp.route("", methods=["GET"])
def cards():
    cards = Card.query.all()
    cards_response = [card.to_json() for card in cards]
    return jsonify(cards_response), 200

# Get one card 
# Note: this is also just for testing purposes in Postman; the FE will never call it.
@cards_bp.route("/<card_id>", methods=["GET"])
def card(card_id):
    card = Card.query.get(card_id)
    if not card: 
        return make_response("", 404)
    return card.to_json(), 200

# Delete one card (some FE event handler should use this)
@cards_bp.route("/<card_id>", methods=["DELETE"])
def delete_card(card_id):
    card = Card.query.get(card_id)
    if not card: 
        return make_response("", 404)

    db.session.delete(card)
    db.session.commit()

    return card.to_json(), 200

# Update a card's likes_count (some FE event handler should use this)
@cards_bp.route("/<card_id>/add_like", methods=["PUT"])
def increment_likes(card_id):
    card = Card.query.get(card_id)
    if card is None:
        return make_response("", 400)

    card.likes_count += 1
    db.session.commit()

    return card.to_json(), 200