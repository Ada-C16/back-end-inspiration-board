from functools import wraps
from app.models.card import Card
from flask import jsonify, request

# Decorator to check if the request body is valid
def require_valid_request_body(endpoint):
    @wraps(endpoint)
    # look into "wraps"
    def fn(*args, **kwargs):
        # look into arg and kwargs
        request_body = request.get_json()

        if request_body["board_id"]== "" and request_body["message"]== "":
            return {"details": "Request body must include board id and message."}, 400
        elif request_body["board_id"]== "":
            return {"details": "Request body must include board id."}, 400
        elif request_body["message"]== "":
            return {"details": "Request body must include message."}, 400
        else:
            return endpoint(*args, request_body=request_body, **kwargs)
    return fn

# Decorator to check if id is an integer and if the card exists.
def require_valid_id(endpoint):
    @wraps(endpoint)
    def fn(*args, card_id, **kwargs):
        try:
            card_id = int(card_id)
        except ValueError:
            return {"message": "Card id needs to be an integer"}, 400

        card = Card.query.get(card_id)

        if not card: 
            return {"message": f"Card {card_id} was not found"}, 404

        return endpoint(*args, card=card, **kwargs)
    return fn