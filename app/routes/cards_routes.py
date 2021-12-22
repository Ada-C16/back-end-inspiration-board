from flask import Blueprint, request, jsonify, make_response
from app.routes.boards_routes import *
from app import db

# example_bp = Blueprint('example_bp', __name__)


cards_bp = Blueprint("cards", __name__, url_prefix="/cards")

# POST /cards Creates a new card.
# returns a dictionary of card information.
# **QUESTION** does it require the board ID to be in the request body?
# Board needs to exist.
# params: message
# likes count could default to 0
# @cards_bp.route("", methods=["POST"])
# def 

# DELETE /cards/<card_id> Deletes a specific card.
# **CONSIDER** return a dictionary with card data.
# @cards_bp.route("/<card_id>", methods=["DELETE"])
# def

# Enhancement ideas: PUT/PATCH cards (edit message), list all cards
# **QUESTION** pretty sure we don't but do we need a get request per specific card?
# **QUESTION** What do we need to validate for each endpoint?