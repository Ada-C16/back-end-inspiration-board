from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.board import Board
from app.models.card import Card

# example_bp = Blueprint('example_bp', __name__)

#created blueprint variables
boards_bp = Blueprint('boards_bp', __name__, url_prefix="/boards")
cards_bp = Blueprint('cards_bp', __name__, url_prefix="/cards")

#<--------------- #GET & POST Boards --------------->
# GET /boards
@boards_bp.route("", methods=["GET"])
def read_board():
    boards = Board.query.all()
    boards_response = []
    for board in boards:
        boards_response.append(board.to_dict())
            
        
    return jsonify(boards_response)

# POST /boards
@boards_bp.route("", methods=["POST"])
def create_board():
    request_body = request.get_json()
    new_board = Board(title=request_body["title"],
        owner=request_body["owner"])

    db.session.add(new_board)
    db.session.commit()

    return jsonify(new_board.to_dict())


#<--------------- #GET & POST card(s) for a single board --------------->

# GET /boards/<board_id>/cards
@boards_bp.route("/<board_id>/cards", methods=["GET"])
def get_cards_for_specific_board(board_id): 

    #get the board b/c we need its details
    #get cards that have that board id 
    #if no cards have that board id, return a specific response 

    board = Board.query.get(board_id) #grab the specific board
    #error check
    if board is None:
        return make_response("not found", 404)

    cards = Card.query.filter(Card.board_id_fk==board_id).all() 
    response = []

    for card in cards:
        #make a helper function in the model "to_dictionary"
            card_dict = {
            "card_id": card.card_id,
            "message": card.message,
            "likes_count": card.likes_count,
            "board_id": card.board_id_fk
            }
            
            response.append(card_dict)
    
    return jsonify(response, 200)

# POST /boards/<board_id>/cards
@boards_bp.route("/<board_id>/cards", methods=["POST"])
def post_card_to_board(board_id):
    board = Board.query.get(board_id) #we grabbed the board for the provided id

    if board is None: #error checking
        return make_response("Board Not Found", 404)

    request_body = request.get_json()
    new_card = Card(message=request_body["message"],
        likes_count=0,
        board_id_fk=board.board_id) #this may raise error

    db.session.add(new_card)
    db.session.commit()

    return make_response(f"Card {new_card.card_id} successfully created", 201)

# DELETE /cards/<card_id>
@cards_bp.route("/<card_id>", methods=["DELETE"])
def delete_a_card(card_id):
    card = Card.query.get(card_id)
    if card is None:
        return make_response(f"Card {card_id} not found", 404)
    # response = {f'Card {card.card_id} successfully deleted'}
    db.session.delete(card)
    db.session.commit()
    return make_response(f'Card {card.card_id} successfully deleted', 200)

# PUT /cards/<card_id>/like
@cards_bp.route("/<card_id>/like", methods=["PUT"])
def update_a_card(card_id):
    card = Card.query.get(card_id)
    
    if card is None:
        return make_response(f"Card {card_id} not found", 404)
    
    # form_data = request.get_json()
    # card.message = form_data["message"]
    card.likes_count+=1
    #card.likes_count = form_data["likes_count"]

    db.session.commit()
    
    response = {
        "card_id": card.card_id,
        "message": card.message,
        "likes_count": card.likes_count,
        "board_id": card.board_id_fk
    }
    return make_response(response, 200)



@cards_bp.route("", methods=["GET"])
def get_cards_for_specific_board_test(): 

    #get the board b/c we need its details
    #get cards that have that board id 
    #if no cards have that board id, return a specific response 

    
    #error check
    

    cards = Card.query.all() 
    response = []

    for card in cards:
        #make a helper function in the model "to_dictionary"
            card_dict = {
            "card_id": card.card_id,
            "message": card.message,
            "likes_count": card.likes_count,
            "board_id": card.board_id_fk
            }
            
            response.append(card_dict)
    
    return jsonify(response, 200)