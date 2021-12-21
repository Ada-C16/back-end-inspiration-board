from flask import Blueprint, request, jsonify, make_response
from sqlalchemy.orm.query import Query
from app import db
from app.models.board import Board
from app.models.card import Card
import requests
from dotenv import load_dotenv
load_dotenv()

cards_bp=Blueprint("card", __name__, url_prefix="/card")


@cards_bp.route("", methods=["POST"])
def create_card():
    request_body = request.get_json()
    new_card= Card(
        message = request_body["message"],
        likes_count = 0
        # Hardcoded likes, could set as default value.
    )
    db.session.add(new_card)
    db.session.commit()

    return jsonify({"message": new_card.message}), 201

@cards_bp.route("", methods=["GET"])
# Update enpoint with board id at a later date
#  "/<board_id>"
def get_all_cards():
    all_cards = Card.query.all()
    output_dicts_list = []
    for card in all_cards:
        output_dicts_list.append(
            {"id":card.card_id,
            "message":card.message
            })

    return jsonify(output_dicts_list), 201


#copy similar import statements as the ones used in video store

#import and load dotenv
#i believe this gets our key-value pairs from .env

#write the blueprint
# example_bp = Blueprint('example_bp', __name__)

#head to init to register the blueprint


#then, start writing the routes


