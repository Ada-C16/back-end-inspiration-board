from flask import Blueprint, request, jsonify, make_response
from sqlalchemy.orm.query import Query
from app import db
from app.models.board import Board
from app.models.card import Card
import requests
from dotenv import load_dotenv
load_dotenv()

boards_bp=Blueprint("board", __name__, url_prefix="/board")

#CREATE ONE BOARD
@boards_bp.route("", methods=["POST"])
def create_board():
    request_body = request.get_json()
    new_board = Board(
        title = request_body["title"],
        owner = request_body["owner"]
    )

    db.session.add(new_board)
    db.session.commit()

    return jsonify({
        "title" : new_board.title,
        "owner" : new_board.owner
    }), 201


#CREATE ONE CARD ON A SPECIFIC BOARD
@boards_bp.route("/<board_ID>", methods=["POST"])
def create_card(board_ID):
    request_body = request.get_json()
    new_card= Card(
        message = request_body["message"],
        likes_count = 0,
        board_id = board_ID
        # Hardcoded likes, could set as default value.
    )
    db.session.add(new_card)
    db.session.commit()

    return jsonify({"message": new_card.message,"board_id": board_ID}), 201

#GET ALL CARDS FOR SPECIFIC BOARD BY ID
@boards_bp.route("/<board_id>", methods=["GET"])
def get_all_cards_from_a_board(board_id):
    #trying to get all cards with same board_id
    all_cards = Card.query.filter_by(board_id=board_id)
    output_dicts_list = []
    for card in all_cards:
        output_dicts_list.append(
            {"id":card.card_id,
            "message":card.message
            })
#the route returns 201, but it's returning an empty list
#not sure why & will revisit in the morning - reid
    return jsonify(output_dicts_list), 201