from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.board import Board

board_bp = Blueprint("board", __name__, url_prefix="/boards")

@board_bp.route("", methods=["POST"])
def create_board():                            
    request_body = request.get_json()[0]
    
    try:
        new_board = Board(title=request_body['title'], owner=request_body['owner'])
        
        db.session.add(new_board)
        db.session.commit()

        return make_response(new_board.make_board_json(),201)
    
    except KeyError as err:
        if "title" in err.args:
            return {"details" : f"Request body must include title with string type."}, 400
        if "owner" in err.args:
            return {"details" : f"Request body must include owner with string type."}, 400


@board_bp.route("/allboards", methods=["GET"])
def get_all_boards():                   # get info of all boards
    all_boards = Board.query.all()
    all_boards_response = [(board.make_board_json()) for board in all_boards]
    return jsonify(all_boards_response), 200


@board_bp.route("/<board_id>", methods=["GET"])
def get_info_of_specific_board(board_id):       # get info of that board 
    try: 
        board = Board.query.get(board_id)

        return board.make_board_json(), 200;
    except:
        return  {"details": f"Board {board_id} not found"}, 404
    
    
@board_bp.route("/<board_id>/allcards", methods=["GET"])
def get_all_cards_specific_board(board_id):       # read all cards of a specific board
    try: 
        board = Board.query.get(board_id)
        
        all_cards_board = [(   
                {"card_id": card.card_id,
                "message": card.message,
                "likes_count": card.likes_count,
                "board_id": board.board_id
                }) for card in board.cards]
        return  jsonify(all_cards_board), 200
    except:
        return  {"details": f"Board {board_id} not found"}, 404

@board_bp.route("/allboards", methods=["DELETE"])
def delete_all_boards():        # delete all boards and all cards
    all_boards = Board.query.all()
    for board in all_boards:
        db.session.delete(board)
        db.session.commit()
    return {"details": "all boards were successfully deleted"}, 200

@board_bp.route("/<board_id>", methods=["DELETE"])
def delete_a_specific_board(board_id):      # delete one boards and all cards of it 
    board = Board.query.get_or_404(board_id)
    db.session.delete(board)
    db.session.commit()
    return {"details": f"Board {board_id} was successfully deleted"}, 200
