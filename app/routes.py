from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.card import Card
from app.models.board import Board

# example_bp = Blueprint('example_bp', __name__)
cards_bp = Blueprint("cards", __name__, url_prefix="/cards")
boards_bp = Blueprint("boards", __name__, url_prefix="/boards")

@cards_bp.route("", methods=["GET","POST"])
def retrieve_cards():
    if request.method == 'GET':
        cards = Card.query.all()
        cards_response = []
        for card in cards:
            cards_response.append(card.card_dict())

        return jsonify(cards_response), 200

    elif request.method == "POST":
        request_body = request.get_json()
        if "message" not in request_body or "likes_count" not in request_body:
            return jsonify ({
                "error meesage": "Invalid data"
            }), 400
        new_card = Card(
            message = request_body["message"],
            likes_count = request_body["likes_count"]
        )

        db.session.add(new_card)
        db.session.commit()

        response_body ={"card": new_card.card_dict()}
        return jsonify(response_body),201

        @cards_bp.route("/<card_id>", methods= ["GET", "PUT","DELETE"])
        def retrieve_get_card(card_id):
            if card is None: 
                return jsonify(None), 404
            elif request.method == "GET":
                
