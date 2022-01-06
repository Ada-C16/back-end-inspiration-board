from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.card import Card

bp = Blueprint("cards", __name__, url_prefix="/cards")

#DELETE
@bp.route("/<card_id>", methods = ["DELETE"])
def delete_card(card_id):
    
    if not card_id.isnumeric():
        return { "Error": "Card id must be numeric."}, 404
    card_id = int(card_id)
    card = Card.query.get(card_id)
    
    if not card:
        return "Card does not exist",404
            
    db.session.delete(card)
    db.session.commit()

    return {
        'message': f'Card {card.card_id} from the board {card.board_id} was successfully deleted'
    }, 200

#LIKE PUT
@bp.route("/<card_id>/like", methods = ["PUT"])
def like_card(card_id):
    card_id = int(card_id)
    card = Card.query.get(card_id)
    card.likes_count +=1

    db.session.commit()
    return ({
        "message": "+1 Like!",
        "likes_count": card.likes_count
        }),200


