from flask import Blueprint, request, jsonify, make_response
from app import db
# from app.models.board import Board
# from app.models.card import Card

# example_bp = Blueprint('example_bp', __name__)
boards_bp = Blueprint("board", __name__, url_prefix="/boards")
cards_bp = Blueprint("cards", __name__, url_prefix="/cards")