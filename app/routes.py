from flask import Blueprint, request, jsonify, make_response
from .models.board import Board
from .models.card import Card
from app import db

board_bp = Blueprint('board', __name__, url_prefix="/board")
card_bp = Blueprint('card', __name__, url_prefix="/card")

@board_bp.route("", methods=["Post"])
def create_new_board():
    new_board = Board(
        name = request_body["name"]
    )

    db.add(new_board)
