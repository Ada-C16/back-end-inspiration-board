from flask import Blueprint, json, request, jsonify, make_response
from app import db
from app.models.card import Card
from app.models.board import Board
import requests
import os

slack_path = "https://slack.com/api/chat.postMessage"

# example_bp = Blueprint('example_bp', __name__)


# beginning CRUD routes code for Card here
# assign cards_bp to the new Blueprint instance
cards_bp = Blueprint("cards", __name__, url_prefix="/cards")


@cards_bp.route("", methods=["POST"])
def post_one_card():
    # request_body will be the user's input, converted to json. it will be a new record
    # for the db, with all fields (a dict)
    request_body = request.get_json()
    if request_body['message'].strip() == "" or 'message' not in request_body:
        return make_response({"details": "Request body must include message."}, 400)
    else:
        # taking info fr request_body and converting it to new Card object
        new_card = Card(message=request_body["message"],
                        likes=0,
                        board_id=request_body["board_id"])
        # committing changes to db
        db.session.add(new_card)
        db.session.commit()
        try:
            query_params = {"channel": "pacific-pals",
            "text": f"Someone just posted a new card, {new_card.message}"}
            header_param = {"Authorization": "Bearer "+ os.environ.get("slack_oauth_token")}
            slack_post_body = requests.post(slack_path, json=query_params, headers= header_param)
        except TypeError:
            pass
        return(new_card.convert_to_dict()), 201



@cards_bp.route("/<card_id>", methods=["GET", "PUT", "DELETE", "PATCH"])
def CRUD_one_card(card_id):
    # either get Card back or None, card here is an object
    card = Card.query.get(card_id)
    if card is None:
        return make_response({"message": f"Card {card_id} was not found"}, 404)

    # PATCH will change just one part of the record, not the whole record

    if request.method == "PATCH":
        form_data = request.get_json()
        if "likes" in form_data:
            card.likes = form_data["likes"]
            db.session.commit()
            return make_response({}, 200)

    if request.method == "DELETE":
        # query db for specific card object by the card id
        # if Card.query.filter_by(id=card_id):
        db.session.delete(card)
        db.session.commit()
        return make_response({'message': f"Card {card.id} was deleted"}, 200)


# beginning CRUD routes code for Board here
# assign boards_bp to the new Blueprint instance
boards_bp = Blueprint("boards", __name__, url_prefix="/boards")


@boards_bp.route("", methods=["POST"])
def post_one_board():
    # request_body will be the user's input, converted to json. it will be a new record
    # for the db, with all fields (a dict)
    request_body = request.get_json()
    if request_body['title'].strip() == "" or 'title' not in request_body:
        return make_response({"details": "Request body must include title."}, 400)
    elif request_body['author'].strip() == "" or 'author' not in request_body:
        return make_response({"details": "Request body must include author."}, 400)
    else:
        # taking info fr request_body and converting it to new Board object
        new_board = Board(title=request_body["title"],
                          author=request_body["author"])
        # committing changes to db
        db.session.add(new_board)
        db.session.commit()
        return(new_board.convert_board_to_dict()), 201

# this end point is returning a list of all Board objects (from the db) that have been jsonified


@boards_bp.route("", methods=["GET"])
def get_all_boards():
    # querying db for all boards and ordering them by title, then storing that list of
    # objects in local boards variable
    boards = Board.query.order_by(Board.title).all()
    boards_response = []
    # looping through each boaard, converting to requested format (dict) and adding to
    # board_response which will be list of dicts
    for board in boards:
        boards_response.append(board.convert_board_to_dict())
    return jsonify(boards_response), 200


@boards_bp.route("/<board_id>/cards", methods=["GET"])
def get_all_cards_for_one_board(board_id):
    if not Board.query.get(board_id):
        return jsonify({"details": f"Board {board_id} was not found"}), 404

    sort_query = request.args.get("sort")
    # if sort query is given, order cards by its query
    if sort_query == "ID":
        # id number order
        cards = Card.query.order_by(Card.id).filter_by(board_id=board_id).all()
    elif sort_query == "Alphabetic":
        # alphabetic order
        cards = Card.query.order_by(
            Card.message).filter_by(board_id=board_id).all()
    elif sort_query == "Likes":
        # likes count order
        cards = Card.query.order_by(
            Card.likes.desc()).filter_by(board_id=board_id).all()
    else:
        # no order specified
        cards = Board.query.get(board_id).cards
    return jsonify([card.convert_to_dict() for card in cards]), 200

    
