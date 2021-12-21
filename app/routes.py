from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.card import Card

# example_bp = Blueprint('example_bp', __name__)
# will need CRUD routes for Card and Board

#beginning CRUD routes code for Card here
# assign videos_bp to the new Blueprint instance
cards_bp = Blueprint("cards", __name__, url_prefix="/cards")
@cards_bp.route("", methods=["POST"])
def post_one_card():
    # request_body will be the user's input, converted to json. it will be a new record 
    # for the db, with all fields (a dict)
    request_body = request.get_json()
    if 'message' not in request_body:
        return make_response({"details": "Request body must include message."}, 400)
    else:
        # taking info fr request_body and converting it to new Card object    
        new_card = Card(message=request_body["message"],
                        increase_likes= 0)
        # committing changes to db
        db.session.add(new_card)
        db.session.commit()
        return(new_card.convert_to_dict()), 201 
                        
# this end point is returning a list of all Card objects (from the db) that have been jsonified
@cards_bp.route("", methods=["GET"])
def get_all_cards():
    # querying db for all cards then storing that list of objects in local cards variable    
    cards = Card.query.all()
    cards_response = []
    # looping through each card, converting to requested format (dict) and adding to
    # card_response which will be list of dicts
    for card in cards:    
        cards_response.append(card.convert_to_dict())
    return jsonify(cards_response), 200