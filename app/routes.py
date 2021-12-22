from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.board import Board
from app.models.card import Card

# example_bp = Blueprint('example_bp', __name__)
boards_bp = Blueprint("boards", __name__, url_prefix="/boards")
@boards_bp.route("", methods = ["POST", "GET"])
def handle_boards():
    if request.method == "POST":
        request_body = request.get_json()
        if "title" not in request_body.keys() or "owner" not in request_body.keys():
                return make_response({"details": "Invalid data"}, 400) 
        else:
            new_board = Board(title=request_body['title'],
                        owner=request_body['owner'])

            db.session.add(new_board)
            db.session.commit()
            return make_response({"board": {
                "id": new_board.board_id, 
                "title":new_board.title,
                'owner':new_board.owner}},
            201)

    elif request.method == "GET":
        boards = Board.query.all()
        boards_response = []

        for board in boards:
            boards_response.append({
                "id": board.board_id,
                "title": board.title,
                "owner": board.owner
            }) 
        return jsonify(boards_response)

# May not be necessary since we need to link all cards to a board but keep for now
@boards_bp.route("/<board_id>", methods = ["GET"])
def handle_board(board_id):
    try:
        board = Board.query.get(board_id)
    except:
        return {"details": "Invalid data"}, 400 # For when you enter /asdjsaiod instead of a num

    if board is None:
        return {"message": f" Board {board_id} not found"}, 404 # For when you enter /5 but there is no board_id of 5 in db
    
    # If valid, then return response abt the specific board
    return {
        "board": {
            "id": board.board_id,
            "title": board.title,
            "owner": board.owner
        }
    }

@boards_bp.route("/<board_id>/cards", methods= ["POST", "GET"])
def handle_boards_cards(board_id):
    board = Board.query.get(board_id)

    if board is None:
        return {"details": f"Board {board_id} not found"}, 404
    
    elif request.method == "POST": # Creates a new card to a board
        request_body = request.get_json()

        if "message" not in request_body or "likes_count" not in request_body or "board_id" not in request_body:
            return {"details": "Invalid data"}, 400
        
        else:
            new_card = Card(message = request_body["message"],
            likes_count = request_body["likes_count"])

            db.session.add(new_card)
            db.session.commit()

            board.cards.append(Card.query.get(new_card.card_id))
            db.session.commit()

            return {
                "card_id": new_card.card_id,
                "message": new_card.message,
                "likes_count": new_card.likes_count,
                "board_id": board.board_id
            }

    elif request.method == "GET": # Reads all cards belonging to a board
        board_cards = []
        for card in board.cards:
            board_cards.append(
                {"card_id": card.card_id,
                "message": card.message,
                "likes_count": card.likes_count,
                "board_id": board.board_id
                })
        return jsonify(board_cards)

    # Need to git commit - added creates a new card + read all cards
