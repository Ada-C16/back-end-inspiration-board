from app import db
from app.models.card import Card
from flask import Blueprint, request, make_response, jsonify
import requests
import os

cards_bp = Blueprint("cards", __name__, url_prefix="/cards")

@cards_bp.route("", methods=["GET"])
def handle_cards():
    cards = Card.query.all()
    card_info = []
    for card in cards:
        card_info.append({
            "id": card.card_id,
            "message": card.message,
            "likes_count": card.likes_count
        })
    return jsonify(card_info), 200

@cards_bp.route("", methods=["POST"])
def post_card():
    request_body = request.get_json()
    try: 
        card = Card(message = request_body["message"])
    except:
        return jsonify("unsuccessful post"), 400
    db.session.add(card)
    db.session.commit()
    return jsonify("successful post"), 201

@cards_bp.route("/<id>/like", methods=["PUT"])
def like_card(id):
    card = Card.query.get(id)
    if card is None:
        return jsonify(""), 404
    card.likes_count += 1
    db.session.commit()
    return jsonify("successful update"), 200

@cards_bp.route("/<id>", methods=["DELETE"])
def delete_card(id):
    card = Card.query.get(id)
    if card is None:
        return jsonify(""), 404
    db.session.delete(card)
    db.session.commit()
    return jsonify(f"successfully deleted {card.message}"), 200 
