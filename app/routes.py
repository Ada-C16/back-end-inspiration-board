from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.card import Card
from app.models.board import Board

# example_bp = Blueprint('example_bp', __name__)
boards_bp = Blueprint ("boards", __name__, url_prefix=("/boards"))
cards_bp = Blueprint ("cards", __name__, url_prefix=("/cards"))

#CARDS
#read - GET
@cards_bp.route("", methods=["GET"])
def get_card():
    cards = Card.query.all()

    response = []
    for card in cards:
        response.append(card.to_dict())

    return jsonify(response), 200

#create - POST

#delete - DELETE



#BOARDS

#read - GET

#create - POST

#delete - DELETE