from flask import Blueprint, request, jsonify, make_response
from app import db

board_bp = Blueprint("board", __name__, url_prefix="/boards")
card_bp = Blueprint("card", __name__, url_prefix="/cards")





