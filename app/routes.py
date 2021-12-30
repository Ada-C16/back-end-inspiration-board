from flask import Blueprint, request, jsonify, make_response
from app import db

board_bp = Blueprint("board", __name__, url_prefix="/boards")
card_bp = Blueprint("card", __name__, url_prefix="/cards")


@board_bp.route("", methods=["POST"])
def create_board():
    return 200

@board_bp.route("", methods=["GET"])
def get_all_boards():
    return 200

@board_bp.route("/<board_id>", methods=["GET"])
def get_specific_board(board_id):
    return 200

@board_bp.route("", methods=["DELETE"])
def delete_all_boards():
    return 200







# @card_bp.route("", methods=["POST"])
# def create_board():
#     return 200

# @card_bp.route("/<card_id>", methods=["DELETE"])
# def delete_specific_card(card_id):
#     return 200

# @card_bp.route("/<card_id>", methods=["PATCH"])
# def update_likes_count(card_id):
#     return 200
    
# @card_bp.route("/<card_id>", methods=["GET"])
# def show_likes_count(card_id):
#     return 200