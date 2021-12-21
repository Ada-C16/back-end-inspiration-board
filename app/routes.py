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
def get_cards():
    cards = Card.query.all()

    response = []
    for card in cards:
        response.append(card.to_dict())

    return jsonify(response), 200

#create - POST
@cards_bp.route("", methods=["POST"])
def create_card():
    request_body = request.get_json()
    try:
        new_card = Card.from_dict(request_body)
        db.session.add(new_card)
        db.session.commit()

        return jsonify(new_card.to_dict()), 201
    except:
        response = {
            "details" : "Invalid request body"
        }

        return jsonify(response), 400

@cards_bp.route("/<card_id>", methods=["GET"])
def get_card(card_id):
    if not card_id.isnumeric():
        return jsonify(None), 400

    card = Card.query.get(card_id)

    if not card:
        return jsonify({'message' : f'Card {card_id} was not found'}), 404

    return jsonify(card.to_dict()), 200
#delete - DELETE



#BOARDS

#read - GET

#create - POST

#delete - DELETE