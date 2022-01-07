from flask import abort, make_response

def get_id(element_id, model):
    element = model.query.get(element_id)
    if element is None:
        return abort(make_response({"message":f"Video {element_id} was not found"}, 404))
    return element
