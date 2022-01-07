from flask import Blueprint, request, jsonify, make_response, abort
from app import db
import app.validate as validate
from app.models.card import Card


cards_bp = Blueprint("cards", __name__, url_prefix="/cards")


@cards_bp.route("/<id>", methods=["DELETE"])
def delete_card(id):
    card_id = validate.valid_id(id)
    card = validate.valid_model(card_id, Card)

    db.session.delete(card)
    db.session.commit()
    response_body = {"details": f"Card {card.id} {card.message} successfully deleted"}
    return make_response(response_body), 200


@cards_bp.route("/<id>", methods=["GET"])
def get_a_card(id):

    card_id = validate.valid_id(id)
    card = validate.valid_model(card_id, Card)

    return card.to_dict()


@cards_bp.route("", methods=["GET"])
def get_all_cards():

    cards = Card.query.all()
    return jsonify([card.to_dict() for card in cards])


@cards_bp.route("/<id>/likes", methods=["PATCH"])
def update_likes(id):

    card_id = validate.valid_id(id)
    card = validate.valid_model(card_id, Card)
    request_body = request.get_json()

    try:
        card.likes_count = request_body["likes_count"]
        db.session.commit()

        return card.to_dict(), 201

    except KeyError:

        return make_response(validate.missing_fields(request_body, Card), 400)
