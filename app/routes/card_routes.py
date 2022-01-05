from app import db
from app.models.card import Card
from app.models.board import Board 
from flask import Blueprint, json, jsonify, make_response, request, abort
from app.common_functions.check_for_id import get_id
from app.common_functions.check_request_body import check_request_body


card_bp = Blueprint("card", __name__, url_prefix="/cards")


# CREATE A CARD 
@card_bp.route("", methods=["POST"])
def create_card():
    request_body = request.get_json()

    request_parameters = ["board_id", "message"]
    check_request_body(request_parameters)

    new_card = Card(
        board_id=request_body["board_id"],
        message=request_body["message"],
        like_count=request_body["like_count"]
        )

    db.session.add(new_card)
    db.session.commit()

    return make_response(new_card.to_dict(), 201)

# READ ALL CARDS
@card_bp.route("", methods=["GET"])
def read_all_cards():
    cards = Card.query.all()

    card_response = []
    for card in cards:
        card_response.append(
            card.to_dict()
        )
    
    return jsonify(card_response)


# DELETE A CARD
@card_bp.route("/<card_id>", methods=["DELETE"])
def delete_card(card_id):
    card = get_id(card_id, Card, str_repr="Card")

    db.session.delete(card)
    db.session.commit()
    return make_response({"id":int(card_id)}, 200)


# UPDATE A CARD 
@card_bp.route("/<card_id>/like", methods=["PUT"])
def update_card(card_id):
    card = get_id(card_id, Card, str_repr="Card")
    card.like_count += 1
    db.session.commit()
    return make_response(card.to_dict(), 200)


    