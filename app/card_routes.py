from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.card import Card

# example_bp = Blueprint('example_bp', __name__)
cards_bp = Blueprint("cards", __name__, url_prefix="/cards")

@cards_bp.route("/<card_id>", methods=["DELETE"])
def delete_card_by_id(card_id):
    card= Card.query.get(card_id)
    if card == None:
        return make_response("Card {card_id} was not found", 404)

    else:
        db.session.delete(card)
        db.session.commit()
        return make_response("Card f{card.id} deleted", 200)

@cards_bp.route("/<card_id>/like", methods=["PUT"])
def add_like_to_card(card_id):
    card= Card.query.get(card_id)
    if card == None:
        return make_response("Card {card_id} was not found", 404)

    else:
        form_data = request.get_json()
        try:
            form_data["likes_count"]
        except:
            return make_response("OOPs try again", 400)
            
        card.likes_count = form_data["likes_count"]
        db.session.commit()

        return make_response("Card {card_id} was liked", 200)