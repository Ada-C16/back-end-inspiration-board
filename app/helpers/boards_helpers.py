from functools import wraps
from app.models.board import Board
from flask import jsonify, request

# Decorator to check if id is an integer and if the board exists.
def require_valid_id(endpoint):
    @wraps(endpoint)
    def fn(*args, board_id, **kwargs):
        try:
            board_id = int(board_id)
        except ValueError:
            return {"message": "Board id needs to be an integer"}, 400

        board = Board.query.get(board_id)

        if not board: 
            return {"message": f"Board {board_id} was not found"}, 404

        return endpoint(*args, board=board, **kwargs)
    return fn

# Decorator to check if the request body is valid
def require_valid_request_body(endpoint):
    @wraps(endpoint)
    # look into "wraps"
    def fn(*args, **kwargs):
        # look into arg and kwargs
        request_body = request.get_json()

        if request_body["title"]== "" and request_body["owner"]== "":
            return {"details": "Request body must include title and owner."}, 400
        elif request_body["title"]== "":
            return {"details": "Request body must include title."}, 400
        elif request_body["owner"]== "":
            return {"details": "Request body must include owner."}, 400
        else:
            return endpoint(*args, request_body=request_body, **kwargs)
    return fn

# Enhancement (or later work...): validate text input for title and owner. Come up with error responses if not str.

def list_of_boards(boards):
    return jsonify([board.board_details() for board in boards])
