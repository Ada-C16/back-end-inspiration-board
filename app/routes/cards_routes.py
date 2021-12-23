from flask import Blueprint, request, jsonify, make_response
from app.helpers.cards_helpers import *
from app.routes.boards_routes import *
from app.models.board import Board
from app.models.card import Card
from app import db

# example_bp = Blueprint('example_bp', __name__)


cards_bp = Blueprint("cards", __name__, url_prefix="/cards")

# DELETE /cards/<card_id> Deletes a specific card.
# **CONSIDER** return a dictionary with card data.
@cards_bp.route("/<card_id>", methods=["DELETE"])
@require_valid_id
def delete_card(card):

    db.session.delete(card)
    db.session.commit()

    return jsonify("Deletion successful"), 200

# Enhancement ideas: PUT/PATCH cards (edit message), list all cards
# **QUESTION** pretty sure we don't but do we need a get request per specific card?
# **QUESTION** What do we need to validate for each endpoint?