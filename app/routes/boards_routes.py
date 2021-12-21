from flask import Blueprint, request, jsonify, make_response
from app.routes.cards_routes import *
from app import db

# example_bp = Blueprint('example_bp', __name__)

boards_bp = Blueprint("boards", __name__, url_prefix="/boards")


# POST /boards Creates a new board.
# params: title (string), name (string)
# returns a dictionary with board data. 
@boards_bp.route("", methods=["POST"])
# def write function here....

# GET /boards Gets a list of all boards.
# returns a dictionary of boards data.
# return empty array if no boards have been created.
@boards_bp.route("", methods=["GET"])
# def 


# GET /boards/<board_id> Gets data for specific board.
# returns a dictionary of the board's data.
@boards_bp.route("/<board_id>", methods=["GET"])

# GET /boards/<board_id>/cards Gets all cards assigned to a specific board.
# returns a dictionary of cards data for the board.
@boards_bp.route("/<board_id>/cards", methods=["GET"])
# def


# Enhancement ideas - DELETE, PUT/PATCH board info