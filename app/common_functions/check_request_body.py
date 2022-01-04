from flask import request, abort, make_response

def chek_request_body(request_body_parameters):
    request_body = request.get_json()
    for parameter in request_body_parameters:
        if parameter not in request_body:
            abort(make_response({"details": f"Request body must include {parameter}."}, 400))