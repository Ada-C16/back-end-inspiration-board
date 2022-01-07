from flask import Blueprint, request, jsonify, make_response
from sqlalchemy.orm.query import Query
from app import db
from app.models.board import Board
from app.models.card import Card
import requests
from dotenv import load_dotenv
load_dotenv()

cards_bp=Blueprint("card", __name__, url_prefix="/card")

#I moved the create card blueprint to board_routes
#Because the endpoint for this should start with board
#like this:
#/board/board_id/card

#I think we might want to move everything over to board, too.
#maybe we actually only want one file for routes?
#because all of the routes for card are written as add-ons to the board endpoint(s)

#@cards_bp.route("", methods=["GET"])
# Update enpoint with board id at a later date
#  "/<board_id>"
"""
def get_all_cards():
    all_cards = Card.query.all()
    output_dicts_list = []
    for card in all_cards:
        output_dicts_list.append(
            {"id":card.card_id,
            "message":card.message
            })

    return jsonify(output_dicts_list), 201
"""




