def get_id(element_id, model):
    element = model.query.get(element_id)
    return element 