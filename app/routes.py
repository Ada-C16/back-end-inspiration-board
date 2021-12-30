from flask import Blueprint, request, jsonify, make_response
from app import db

# example_bp = Blueprint('example_bp', __name__)
board_bp = Blueprint('board_bp', __name__, url_prefix="/boards")
card_bp = Blueprint('card_bp', __name__, url_prefix="/cards")


####---------------------------------------------------####
####----------------- BOARD ENDPOINTS -----------------####
####---------------------------------------------------####

# ---1----
# Route: "/boards"
# Method: GET
# 1. boards_response = []
# 2. database request -> boards = Board.query....
# 3. turn response into a list of dictionaries?
#           - [{"board_id":board_id, "owner":owner, "title": title}, {}, {}]
# 4. return jsonify(boards_response, 200)


# @board_bp.route("", methods=["GET"])
# def create_board():
#     boards_response = []
#     boards = Board.query
#     

# ---2----
# Route: "/boards/<board_id>"
# Method: GET
# 1. Data check -> 
#       - is it numeric? make_response({"message" : "Please enter a valid board id"}, 400)
#       - does board_id exist? make_response({"message" : f"{entity} {id} was not found"}, 404)
# 2. database query 
#       - cards = db.session.query(Card).filter(Card.board_id==board_id)
# 3. cards_response = []
# 4. turn response into a list of dictionaries
#       - [{"card_id":card_id, "message":owner, "likes_count": likes_count}, {}, {}]
# 4. return jsonify(cards_response, 200)

# ---6----
# Route: "/boards"
# Method: POST
# 1. request_body = request.get_json()
# 2. check request data - make sure title and owner are present
# 3. create new board 
        # - new_board = Board(title=request_body["title"], owner=request_body["owner"])
# 4. db.session.add(new_board)
# 5. db.session.commit()
# 4. return ....what to return here?? dict of new board? + 200 OK?


# ---7----
# Route: "/boards"
# Method: DELETE
# 1. database query boards
# 2. If board in query result does not equal the defualt board:
        # - db.session.delete(board)
        # - db.session.commit()
        # Note here we want to delete all boards but one, we want to leave a defualt board like the example
# 3. make_response("All but default board have been deleted", 200)

####---------------------------------------------------####
####------------------ CARD ENDPOINTS -----------------####
####---------------------------------------------------####

# ---3----
# Route: "/cards/<card_id>"
# Method: PUT
# 1. Data check -> 
#       - is it numeric? make_response({"message" : "Please enter a valid board id"}, 400)
#       - does card_id exist? make_response({"message" : f"{entity} {id} was not found"}, 404)
# 2. database query by card_id
        # - card=Card.query.get(card_id)
        # - card.like_count +=1
# 3. make_response("Successfully updated like count", 200)

# ---4----
# Route: "/cards/<card_id>"
# Method: DELETE
# 1. Data check -> 
#       - is it numeric? make_response({"message" : "Please enter a valid board id"}, 400)
#       - does board_id exist? make_response({"message" : f"{entity} {id} was not found"}, 404)
# 2. database query by card_id
        # - Card.query(card_id)
# 3. db.session.delete(card)
# 4. db.session.commit()
# 5. make_response("Successfully deleted card", 200)

# ---5----
# Route: "/cards/<card_id>"
# Method: POST
# 1. request_body = request.get_json()
# 2. check request data - make sure message is present
# 3. create new card 
        # - new_card = Card(message=request_body["message"])
# 4. db.session.add(new_card)
# 5. db.session.commit()
# 4. return ....what to return here?? dict of new card? + 200 OK?



