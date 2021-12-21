from flask import Blueprint, request, jsonify, make_response
from app import db

# example_bp = Blueprint('example_bp', __name__)
# will need CRUD routes for Card and Board

#beginning CRUD routes code for Card here
# assign videos_bp to the new Blueprint instance
cards_bp = Blueprint("cards", __name__, url_prefix="/cards")
@cards_bp.route("", methods=["POST"])
def post_one_card():
    # request_body will be the user's input, converted to json. it will be a new record 
    # for the db, with all fields (a dict)
    request_body = request.get_json()
