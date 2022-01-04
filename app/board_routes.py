from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.board import Board
from app.models.card import Card

board_bp = Blueprint("board", __name__, url_prefix="/boards")


# Create a new board, by filling out a form. The form includes "title" and "owner" name of the board.

# See an error message if I try to make a new board with an empty/blank/invalid/missing "title" or "owner" input.

# All error messages can look like a new section on the screen, a red outline around the input field, and/or disabling the input, as long as it's visible
#HELPER FUNCTIONS

# def valid_int(number, parameter_type):
#     try:
#         number = int(number)
#     except:
#         abort(400, {"error": f"{parameter_type} must be an int"})


def get_id(element_id, model):
    element = model.query.get(element_id)
    return element 

#BOARD ROUTES
# CREATE BOARD
@board_bp.route("", methods=["POST"])
def create_board():
    request_body = request.get_json()
    if "title" not in request_body:
        return {"details":"Missing title."}, 400
    elif "owner" not in request_body:
        return {"details":"Missing owner_name."}, 400
    
    new_board = Board(
        title=request_body["title"],
        owner=request_body["owner"],
    )

    db.session.add(new_board)
    db.session.commit()

    return make_response(f"Board {new_board.id} created!"), 201

# READ ALL BOARDS
@board_bp.route("", methods=["GET"])
def read_all_boards():
    boards = Board.query.all()
    boards_response = []
    for board in boards:
        boards_response.append(
            board.to_dict()
        )

    return jsonify(boards_response)

# READ ONE BOARD
@board_bp.route("<board_id>/cards", methods=["POST"])
def read_board(board_id):
    board = get_id(board_id, Board)
    response_body = board.read_cards()
    return jsonify(response_body), 200


#CARD ROUTES

# @board_bp.route("/<board_id>/cards", methods=["POST"])
# def create_card(board_id):


    
    
    
#     current_task.goal_id = goal.goal_id

# HELPER FUNCTIONS
# def valid_int(number, parameter_type):
#     try:
#         number = int(number)
#     except:
#         abort(400, {"error": f"{parameter_type} must be an int"})


# def get_customer_from_id(customer_id):
#     valid_int(customer_id, "customer_id")
#     customer = Customer.query.get(customer_id)
#     if not customer:
#         abort(make_response(
#             {"message": f"Customer {customer_id} was not found"}, 404))

#     return customer

# @customer_bp.route("", methods =["POST"])
# def create_customer():
#     request_body = request.get_json()
#     if "name" not in request_body: 
#         return {"details":"Request body must include name."}, 400
#     elif "postal_code" not in request_body:
#         return {"details":"Request body must include postal_code."}, 400
#     elif "phone" not in request_body:
#         return {"details": "Request body must include phone."}, 400
#     
#         new_customer = Customer(
#             name=request_body["name"],
#             postal_code=request_body["postal_code"],
#             phone=request_body["phone"],
#         )

#         db.session.add(new_customer)
#         db.session.commit()

#         return {"id":new_customer.id}, 201

