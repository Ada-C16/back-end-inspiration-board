from app import db
from flask import make_response
from flask_sqlalchemy import abort
from app.models.board import Board
from app.models.card import Card

def valid_id(model, id):
    """Parameters: Model type and id of model.
        Returns instance of model with matching ID.
        Returns 404 and custom message if model with given ID does not exist."""
    try:
        id = int(id)
    except:
        abort(400, {"error": "invalid id"})

    model = model.query.get(id)

    if not model: 
        abort(make_response({"message": "not found"}, 404))

    return model

def valid_input(request_body, model): 
    """Input: JSON version of request and type of model.
    Checks request body for required input per model.
    Returns 400 with needed input if missing."""
    if model == Board: 
        required_input = ["title", "owner"]

    if model == Card:
        required_input = ["message", "board_id"]

    for input in required_input:
        if input not in request_body:
            abort(make_response({"details": f"Request body must include {input}."}, 400))