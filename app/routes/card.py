from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.card import Card

# example_bp = Blueprint('example_bp', __name__)
cards_bp = Blueprint("cards", __name__, url_prefix="/cards")

@cards_bp.route("/<card_id>", methods=["DELETE"])
def delete_card_by_id(card_id):
    card = Card.query.get(card_id)
    if card == None:
        return jsonify("Card {card_id} was not found", 404)

    else:
        db.session.delete(card)
        db.session.commit()
        return jsonify(card.create_card_dict(), 200)

@cards_bp.route("/<card_id>/like", methods=["PATCH"])
def add_like_to_card(card_id):
    card = Card.query.get(card_id)
    if card == None:
        return jsonify("Card {card_id} was not found", 404)
# are we expecting the front end to send a specfic number or will it be sending
# a +1 to the likes_count and we need to incremement the variable in the database
    else:
        form_data = request.get_json()
        try:
            form_data["likes_count"]
        except:
            return jsonify("Oops try again", 400)
            
        card.likes_count = form_data["likes_count"]
        db.session.commit()

        return jsonify(card.create_card_dict(), 200)