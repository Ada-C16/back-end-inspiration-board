from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.board import Board
# from app.models.board import Card

board_bp = Blueprint("board", __name__, url_prefix="/boards")
card_bp = Blueprint("card", __name__, url_prefix="/cards")


@board_bp.route("", methods=["POST"])
def create_board():
    request_body = request.get_json()
    
    try:
        new_board = Board(title=request_body[0]['title'], owner=request_body[0]['owner'])
        
        db.session.add(new_board)
        db.session.commit()

        return make_response(
                {"board id": new_board.board_id, 
                "title":new_board.title,
                'owner':new_board.owner},
            201)
    
    except KeyError as err:
        if "title" in err.args:
            return {"details" : f"Request body must include title with string type."}, 400
        if "owner" in err.args:
            return {"details" : f"Request body must include owner with string type."}, 400


@board_bp.route("", methods=["GET"])
def get_all_boards():
    all_boards = Board.query.all()
    all_boards_response = []

    for board in all_boards:
        all_boards_response.append({
            "board id": board.board_id,
            "title": board.title,
            "owner": board.owner
        }) 
    return jsonify(all_boards_response), 200


@board_bp.route("/<board_id>", methods=["GET"])
def get_info_of_specific_board(board_id):  
    try: 
        board = Board.query.get(board_id)

        return {
            "id": board_id,
            "title": board.title,
            "owner": board.owner
        }, 200;
    except:
        return  {"details": f"Board {board_id} not found"}, 404
    
    
@board_bp.route("/<board_id>/cards", methods=["GET"])
def get_all_cards_specific_board(board_id):       # read all cards of a specific board
    try: 
        board = Board.query.get(board_id)
        
        cards_board = []
        for card in board.cards:
            cards_board.append(   
                {"card_id": card.card_id,
                "message": card.message,
                "likes_count": card.likes_count,
                "board_id": board.board_id
                })
    except:
        return  {"details": f"Board {board_id} not found"}, 404
    
    
@board_bp.route("", methods=["DELETE"])
def delete_all_boards():
    all_boards = Board.query.all()
    for board in all_boards:
        db.session.delete(board)
        db.session.commit()
    return {"details": "all boards were successfully deleted"}, 200

@board_bp.route("<board_id>", methods=["DELETE"])
def delete_a_specific_board(board_id):
    board = Board.query.get_or_404(board_id)
    db.session.delete(board)
    db.session.commit()
    return {"details": f"Board {board_id} was successfully deleted"}, 200
