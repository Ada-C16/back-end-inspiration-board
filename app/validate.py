from flask import abort, make_response
from app.models.board import Board


def valid_id(id):
    try:
        id = int(id)
    except ValueError:
        abort(400)
    return id


def valid_model(id, model):
    valid = model.query.get(id)

    if not valid:
        abort(make_response({"message": f"{id} was not found"}, 404))
    return valid



def missing_fields(request_body, model):
    for field in model.required_fields:
        if field not in request_body:
            return {"details": f"Request body must include {field}."}
    return False
