from flask import Blueprint, request, jsonify, make_response
from sqlalchemy.orm.query import Query
from app import db
from app.models.board import Board
from app.models.card import Card
import requests
from dotenv import load_dotenv
load_dotenv()
from functools import wraps

boards_bp=Blueprint("board", __name__, url_prefix="/board")

# Decorator for validation
# Can be used for any route that has <board_ID>
# Updated routes to use <board_ID> because <board_id> was overlapping with model values. 
# Challange someone to try something similar for GET by card_ID
# Will explain decorators, args/kwargs, wraps tomorrow. 

def validate_board(board_identity):
    @wraps(board_identity)
    def test_for_board (*args, board_ID, **kwargs):
        if not board_ID.isnumeric(): 
            return ({"message":f"Board {board_ID} does not exist.",}), 404
        
        board_check = Board.query.get(board_ID)
        if board_check:
            return board_identity (*args, board_ID, **kwargs)
        else:
            return ({"message":f"Board {board_ID} does not exist",}), 404
    return test_for_board

def validate_card(card_identity):
    @wraps(card_identity)
    def test_for_card (*args, card_ID, **kwargs):
        if not card_ID.isnumeric(): 
            return ({"message":f"Card {card_ID} does not exist.",}), 404
        
        card_check = Card.query.get(card_ID)
        if card_check:
            return card_identity (*args, card_ID, **kwargs)
        else:
            return ({"message":f"Card {card_ID} does not exist",}), 404
    return test_for_card


#CREATE ONE BOARD
@boards_bp.route("", methods=["POST"])
def create_board():
    request_body = request.get_json()
    
    if (("title" not in request_body.keys()) or 
        ("owner" not in request_body.keys())):
        return jsonify("Board not created. Must supply title and owner."), 404
    
    new_board = Board(
        title = request_body["title"],
        owner = request_body["owner"]
    )

    db.session.add(new_board)
    db.session.commit()

    return jsonify({
        "title" : new_board.title,
        "owner" : new_board.owner,
        "id" : new_board.board_id
    }), 201


#CREATE ONE CARD ON A SPECIFIC BOARD
@boards_bp.route("/<board_ID>", methods=["POST"])
@validate_board
def create_card(board_ID):
    request_body = request.get_json()
    
    if ("message" not in request_body.keys()):
        return jsonify ()
    
    new_card= Card(
        message = request_body["message"],
        likes_count = 0,
        board_id = board_ID
    )
    db.session.add(new_card)
    db.session.commit()

    return jsonify({"message": new_card.message,
                    "board_id": new_card.board_id, 
                    "likes_count":new_card.likes_count}), 201

#GET ALL CARDS FOR SPECIFIC BOARD BY ID
@boards_bp.route("/<board_ID>/cards", methods=["GET"])
@validate_board
def get_all_cards_from_a_board(board_id):
    all_cards = Card.query.filter_by(board_id=board_id)
    output_dicts_list = []
    for card in all_cards:
        output_dicts_list.append({
            "card_id":card.card_id,
            "message":card.message,
            "board_id":card.board_id,
            "likes_count":card.likes_count
            #we want to return the likes_count in this dictionary here so that each card like count renders correctly
            })
    return jsonify(output_dicts_list), 201


#GET ONE CARD FOR SPECIFIC BOARD BY ID
@boards_bp.route("/<board_ID>/cards/<card_ID>", methods=["GET"])
@validate_board
@validate_card
def get_one_card_from_a_board(board_ID, card_ID):
    #should we actually fetch this by board_ID and card_ID? Does it matter?
    card = Card.query.get(card_ID)
    
    return jsonify({
            "card_id":card.card_id,
            "message":card.message,
            "board_id":card.board_id,
            "likes_count":card.likes_count
            }), 201

# GET ALL BOARDS
@boards_bp.route("", methods=["GET"])
def get_all_boards():
    boards = Board.query.all()

    response_body = []

    for board in boards:
        response_body.append(
            {"id" : board.board_id,
            "title" : board.title,
            "owner" : board.owner}
        )

    return jsonify(response_body), 200

# GET ONE BOARD BY SUPPLYING board_id
@boards_bp.route("/<board_ID>", methods=["GET"])
@validate_board
def get_one_board(board_ID):
    board = Board.query.get(board_ID)

    if board is None:
        return jsonify(None),404
    
    response_body = {
        "id" : board.board_id,
        "title" : board.title,
        "owner" : board.owner
    }

    return jsonify(response_body), 200

@boards_bp.route("/<board_ID>", methods=["DELETE"])
@validate_board
def delete_one_whole_entire_board(board_ID):
    board = Board.query.get(board_ID)
    db.session.delete(board)
    db.session.commit()

    #not sure if we need this?
    all_cards = Card.query.filter_by(board_id=board_ID)
    for card in all_cards:
        db.session.delete(card)
        db.session.commit()
            
    response = {"message": f"Board {board.title} was deleted."}
    return response, 200

@boards_bp.route("/<board_ID>/cards/<card_ID>", methods=["DELETE"])
@validate_board
def delete_one_teeny_tiny_card(board_ID, card_ID):
    card = Card.query.get(card_ID)
    if card:
        db.session.delete(card)
        db.session.commit()
        response = {"message": f"Card {card.card_id} was deleted."}
        return response, 200
    return {"message": f"Card id {card_ID} isn't real."},400


#PATCH REQUEST TO INCREMENT CARD.LIKES_COUNT BY 1
@boards_bp.route("/<board_ID>/cards/<card_ID>", methods=["PATCH"])
@validate_board
def add_one_to_likes_count(board_ID, card_ID):
    card = Card.query.get(card_ID)
    if card:
        card.likes_count = int(card.likes_count) + 1
        db.session.commit()
        response = {"message": f"Card {card.card_id} likes count was updated to {card.likes_count}"}
        return response, 200
    return {"message": f"Card id {card_ID} isn't real."},400