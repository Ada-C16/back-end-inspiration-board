from flask import Blueprint, request, jsonify, make_response
from flask.globals import request 
from app.models.board import Board
from app.models.card import Card
from app import db

# example_bp = Blueprint('example_bp', __name__)

##################################
########## BOARD ROUTES ##########
##################################
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

#get one board
@board_bp.route("/<board_id>", methods=["GET"])
def get_board(board_id):
    board = Board.query.get(board_id)

    if board is None:
        return jsonify(None), 404
    
    response_body = {
        "board": (board.to_dict())
    }
    
    return jsonify(response_body), 200

@board_bp.route("/<board_id>", methods=["PUT", "PATCH"]) 
def update_board(board_id):
    request_body = request.get_json()

    board = Board.query.get(board_id)

    if not board:
        return {"message": f"Board {board_id} was not found"}, 404 

    if "title" not in request_body or "owner" not in request_body:
        return {"details":  "Invalid request"}, 400 

    board.title =  request_body["title"]
    board.owner = request_body["owner"]
    
    db.session.commit()
    return board.to_dict(), 200

@board_bp.route("/<board_id>", methods=["DELETE"])
def delete_board(board_id): 
    board = Board.query.get(board_id)

    if not board:
        return {"message": f"Board {board_id} was not found"}, 404

    db.session.delete(board)
    db.session.commit()

    return {"board_id": board.id}, 200
##################################
##################################
########## CARD ROUTES ##########
##################################
##################################
card_bp = Blueprint("card_bp", __name__, url_prefix="/card")

@card_bp.route("", methods=["POST"])
def create_card():
    request_body = request.get_json()
    
    missing = ""
    if "message" not in request_body:
        missing = "title"
    elif "likes_count" not in request_body:
        missing = "owner"
    if missing:
        return{"details": f"Request body must include {missing}."}, 400

    new_card = Card(
        message=request_body["message"],
        likes_count=request_body["likes_count"],
    )

    db.session.add(new_card)
    db.session.commit()

    return {"id": new_card.card_id}, 201

#get one card 
@card_bp.route("/<card_id>", methods=["GET"])
def get_card(card_id):
    card = Card.query.get(card_id)

    if card is None:
        return jsonify(None), 404
    
    response_body = {
        "card": (card.to_dict())
    }
    
    return jsonify(response_body), 200

@card_bp.route("", methods=["GET"])
def read_cards():
    cards = Card.query.all()

    response_body = []

    if not cards:
        return jsonify([]), 200

    for card in cards:
        response_body.append(card.to_dict())

    return jsonify(response_body), 200
#nested route that gets a specific board and all its cards 
@board_bp.route("/<board_id>/card", methods=["GET", "POST"])
def handle_board_card(board_id):
    board = Board.query.get(board_id=board_id)
    if board is None:
        return make_response("Board not found", 404)

    if request.method == "POST":
        request_body = request.get_json()
        new_card = Card(
            message=request_body["message"],
            likes_count=request_body["likes_count"],
            )
        db.session.add(new_card)
        db.session.commit()
        return make_response(f"Card {new_card.message} by {new_card.board.title} successfully created", 201)

@card_bp.route("/<card_id>", methods=["PUT", "PATCH"])  
def update_card(card_id):
    request_body = request.get_json()

    card = Card.query.get(card_id)

    if not card:
        return {"message": f"Card {card_id} was not found"}, 404 

    if "message" not in request_body or "likes_count" not in request_body:
        return {"details":  "Invalid request"}, 400 

    card.message =  request_body["message"]
    card.likes_count = request_body["likes_count"]
    
    db.session.commit()
    return card.to_dict(), 200

@card_bp.route("/<card_id>", methods=["DELETE"])
def delete_card(card_id): 
    card = Card.query.get(card_id)

    if not card:
        return {"message": f"Card {card_id} was not found"}, 404

    db.session.delete(card)
    db.session.commit()

    return {"card_id": card.id}, 200

