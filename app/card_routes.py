from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.board import Board
from app.models.card import Card
from .helper_functions import get_id

card_bp = Blueprint("card", __name__, url_prefix="/cards")

# # DELETE SINGLE CARD
@card_bp.route("/<card_id>", methods=["DELETE"])
def delete_card(card_id): 
    card = get_id(card_id, Card)
    db.session.delete(card)
    db.session.commit()

    return "This card will miss you :(", 200


