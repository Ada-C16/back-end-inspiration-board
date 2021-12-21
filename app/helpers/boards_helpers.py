from functools import wraps
from app.models.board import Board
from flask import jsonify, request

# Decorator to check if the request body is valid
def require_valid_request_body(endpoint):
    @wraps(endpoint)
    # look into "wraps"
    def fn(*args, **kwargs):
        # look into arg and kwargs
        request_body = request.get_json()

        if "title" not in request_body and "owner" not in request_body:
            return {"details": "Request body must include title and owner."}, 400
        elif "title" not in request_body:
            return {"details": "Request body must include title."}, 400
        elif "owner" not in request_body:
            return {"details": "Request body must include owner."}, 400
        else:
            return endpoint(*args, request_body=request_body, **kwargs)
    return fn

# Enhancement (or later work...): validate text input for title and owner. Come up with error responses if not str.
