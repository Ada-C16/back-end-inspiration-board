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
        abort(make_response({"message": f"{model.model_string} {id} was not found"}, 404))

    return model