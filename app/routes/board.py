from flask import Blueprint, jsonify, request

from app import db
from app.models.board import Board
from app.models.card import Card

boards_bp = Blueprint("boards_bp", __name__, url_prefix="/boards")

@boards_bp.route("", methods=["GET"])
def get_boards():
    boards = Board.query.all()