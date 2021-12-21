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


@cards_bp.route("/<card_id>", methods=["GET", "PUT", "DELETE", "PATCH"])
def CRUD_one_card(card_id):
    card = Card.query.get(card_id) #either get Card back or None, card here is an object
    if card is None:
        return make_response({"message": f"Card {card_id} was not found"}, 404)

    # PATCH will change just one part of the record, not the whole record
    # not required but adding a patch for total_inventory on 11.9.21

    # if request.method == "PATCH":
    #     form_data = request.get_json()
    # if "increase_likes" in form_data:
    #     card.increase_likes = form_data["increase_likes"]
    # db.session.commit()
    # return make_response({"video": {"id": video.id,
    #                 "title": video.title,
    #                 "release_date": video.release_date,
    #                 "total_inventory": video.total_inventory}}, 200)

    if request.method == "DELETE":
    # query db for specific card object by the card id
        if Card.query.filter_by(id=card_id):
            db.session.delete(card)
            db.session.commit()
        return make_response({'message': f"Card {card.id} was deleted"}, 200)