
from app import db
from app.models.board import Board
from app.models.card import Card
from flask import Blueprint, request, jsonify
import os 

card_bp = Blueprint("card", __name__, url_prefix="/cards")

# FE ACTION: Submit button on card
## Create a card 
# expected {"message": "loremipsum"} => error message or created card object
@card_bp.route("", methods=["POST"])
def create_card():
    request_body = request.get_json()
    if not request_body or "message" not in request_body:
        return jsonify({"details": "Request must include a message."}), 400
    elif  len(request_body["message"]) < 1: 
        return jsonify({"details": "Message can not be empty"}), 400
    elif len(request_body["message"]) > 40: 
        return jsonify({"details": "Message exceeds 40 characters limit"}), 400
    else : 
        new_card = Card(
            message = request_body["message"],
            likes_count = 0
        )
        db.session.add(new_card)
        db.session.commit() 
        response_body = build_a_card_response(new_card)
        return jsonify(response_body), 201

#FE Action ??
## Reads a single card with current message and likes count
# Expected: card_id # => error message or card object 
@card_bp.route("/<card_id>", methods=["GET"])
def show_likes_count(card_id):
    if not card_id.isnumeric():
        return jsonify({"details":f"{card_id} is invalid, card id must be numerical"}),400
    card = Card.query.get(card_id)
    if card == None:
        return jsonify({"details": f"Card {card_id} was not found"}), 404 
    else:
        response_body = build_a_card_response(card)
        return jsonify(response_body),200

#FE Action: +1 button on a card
# Updates a card likes count by 1 
## expected card_id# {likes_count: 1} => error message or updated card object
@card_bp.route("/<card_id>", methods=["PATCH"])
def update_likes_count(card_id):
    request_body = request.get_json()
    if not card_id.isnumeric():
        return jsonify({"details":f"{card_id} is invalid, card id must be numerical"}),400
    if not request_body or "likes_count" not in request_body:
        return jsonify({"details": "Request must include likes_count."}), 400
    card = Card.query.get(card_id)
    if card == None:
        return jsonify({"details": f"Card {card_id} was not found"}), 404 
    else:
        card.likes_count = card.likes_count + request_body["likes_count"]
    db.session.commit()
    response_body = build_a_card_response(card)
    return jsonify(response_body),200

#FE Action: delete button on a card 
# Delete specific card
# expected: card_id # => error message or success message 
@card_bp.route("/<card_id>", methods=["DELETE"])
def delete_specific_card(card_id):
    if not card_id.isnumeric():
        return jsonify({"details":f"{card_id} is invalid, card id must be numerical"}),400
    card = Card.query.get(card_id)
    if card == None:
        return jsonify({"details": f"Card {card_id} was not found"}), 404
    else:
        db.session.delete(card)
        db.session.commit()
        return jsonify({"details": f"Card {card_id} was successfully deleted"}), 200
    
##Helpers 
def build_a_card_response(card):
    response = {
        "id": card.card_id, 
        "message": card.message,
        "likes_count": card.likes_count,
        }
    return response

def build_cards_response(cards):
    response = []
    for card in cards:
        response.append({
        "id": card.card_id, 
        "message": card.message,
        "likes-count": card.likes_count,
        })
    return response 

#FE Action: None 
#Testing card creation 
# Will need to get cards in relations to a board for project 
# expected:nothing => all card objects 
@card_bp.route("", methods = ["GET"])
def get_all_cards():
        cards = Card.query.all()
        response_body = build_cards_response(cards)
        return jsonify(response_body),200

#CARD MODEL 
# class Card(db.Model):
    # card_id = db.Column(db.Integer, primary_key=True)
    # message = db.Column(db.String)
    # likes_count = db.Column(db.Integer)
    # board_id = db.Column(db.Integer, db.ForeignKey('board.board_id'))
    # board = db.relationship("Card", back_populates="cards")    