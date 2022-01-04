from app import db
from app.models.card import Card
from app.models.board import Board 
from flask import Blueprint, json, jsonify, make_response, request, abort


card_bp = Blueprint("card", __name__, url_prefix="/cards")

def valid_int(number, parameter_type):
    try:
        int(number)
    except:
        abort(make_response({"error": f"{parameter_type} must be an int"}, 400))

def get_id(id, model, str_repr):
    valid_int(id, "id")

    model_variable = model.query.get(id)
    if not model_variable:        
        abort(make_response({"message": f"{str_repr} {id} was not found"}, 404))
    return model_variable


def check_request_body(request_body_parameters):
    request_body = request.get_json()
    for parameter in request_body_parameters:
        if parameter not in request_body:
            abort(make_response({"details": f"Request body must include {parameter}."}, 400))

def read_all(model):
    all_data = model.query.all()

    response = []
    for data in all_data:
        response.append(
            data.to_dict()
        )
    return response

#CREATE A CARD 
@card_bp.route("", methods=["POST"])
def create_card():
    request_body = request.get_json()

    request_parameters = ["board_id", "message", "like_count"]
    check_request_body(request_parameters)

    new_card = Card(
        board_id=request_body["board_id"],
        message=request_body["message"],
        like_count=request_body["like_count"]
        )

    db.session.add(new_card)
    db.session.commit()

    return make_response(new_card.to_dict(), 201)

#READ ALL CARDS
@card_bp.route("", methods=["GET"])
def read_all_cards():
    cards = Card.query.all()

    card_response = []
    for card in cards:
        card_response.append(
            card.to_dict()
        )
    
    return jsonify(card_response)


#DELETE A CARD
@card_bp.route("/<card_id>", methods=["DELETE"])
def delete_card(card_id):
    card = get_id(card_id, Card, str_repr="Card")

    db.session.delete(card)
    db.session.commit()
    return make_response({"id":int(card_id)}, 200)


#UPDATE A CARD 

@card_bp.route("/<card_id>/like", methods=["PUT"])
def update_card(card_id):
    card = get_id(card_id, Card, str_repr="Card")
    request_body = request.get_json()

    # if "like_count" in request_body:
    card.like_count = card.like_count+1

    
    db.session.commit()
    return make_response({"card": card})


    