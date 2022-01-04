from flask import make_response, abort

def valid_int(number, parameter_type):
    try:
        int(number)
    except:
        abort(make_response({"error": f"{parameter_type} must be an int"}, 400))

def get_id(id, model, str_repr):
    valid_int(id, "id")

    model_variable = model.query.get(id)
    if not model_variable:        
        abort(make_response({"message": f"{str_repr} {id} was not found"}, 404))
    return model_variable