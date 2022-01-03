from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.card import Card
from app.models.board import Board

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


@boards_bp.route("/<board_id>", methods=["GET", "PUT", "DELETE", "PATCH"])
def CRUD_one_board(board_id):
    # either get Board back fr db or None, board here is an object
    board = Board.query.get(board_id)
    if board is None:
        return make_response({"message": f"Board {board_id} was not found"}, 404)
    if request.method == "GET":
        return board.convert_board_to_dict()

    if request.method == "DELETE":
        # query db for specific board object by the board id
        # if Board.query.filter_by(id=board_id):
        db.session.delete(board)
        db.session.commit()
        return make_response({'message': f"Board {board.id} was deleted"}, 200)


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

    # query Board table using board_id
    # board_query = Board.query.get(board_id)
    # # guard clause to check the board_id is valid
    # if board_query:
    # # query and return all Card objects with the specified board_id as their foreign key
    # #     cards_for_boards = Card.query.filter_by(board_id=board_id).all()
    # # iterate through the list of returned Card objects, use helper function to convert to dict
    # # and store in list named cards_response.  Need objects to be dicts so front end can access their data
    #     cards_response = []
    #     for card in cards_for_boards:
    #         cards_response.append(card.convert_to_dict())
    #     return jsonify(cards_response), 200
    # else:
    #     return jsonify({"message": f"Board {board_id} was not found"}), 404
