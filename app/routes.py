from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.board import Board
from app.models.card import Card

# example_bp = Blueprint('example_bp', __name__)
boards_bp = Blueprint("boards", __name__, url_prefix="/boards")
@boards_bp.route("", methods = ["POST", "GET"])
def handle_boards():
    if request.method == "POST":
        request_body = request.get_json()
        if "title" not in request_body.keys() or "owner" not in request_body.keys():
                return make_response({"details": "Invalid data"}, 400) 
        else:
            new_board = Board(title=request_body['title'],
                        owner=request_body['owner'])
            db.session.add(new_board)
            db.session.commit()
            return make_response({"board": {"id": new_board.board_id, 
            "title":new_board.title,'owner':new_board.owner}},201)
    elif request.method == "GET":
        boards = Board.query.all()
        boards_response = []

        for board in boards:
            boards_response.append({
                "id": board.board_id,
                "title": board.title,
                "owner": board.owner
            }) 
        return jsonify(boards_response)

@boards_bp.route("/<board_id>", methods = ["GET"])
def handle_board(board_id):
    try:
        board = Board.query.get(board_id)
    except:
        return {"details": "Invalid data"}, 400 # For when you enter /asdjsaiod instead of a num

    if board is None:
        return {"message": f" Board {board_id} not found"}, 404 # For when you enter /5 but there is no board_id of 5 in db
    
    # If valid, then return response abt the specifoc board
    return {
        "board": {
            "id": board.board_id,
            "title": board.title,
            "owner": board.owner
        }
    }

