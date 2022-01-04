from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.board import Board
from app.models.card import Card

card_bp = Blueprint("card", __name__, url_prefix="/cards")

# @card_bp.route("/<board_id>/cards", methods=["POST"])
# def create_card(board_id):
