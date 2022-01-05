from app.models.board import Board
from app.models.card import Card
from flask import jsonify

BOARD_ID = 1
TITLE = "Test Board"
OWNER = "Test Group"

CARD_ID = 1
MESSAGE = "Test message"
LIKES_COUNT = 0

#rename folder
#test GET all boards, board by id and cards per board
#test POST a new board and a new card

#GET ALL BOARDS AND BY ID
def test_get_boards_no_boards_saved(client):
    # Act
    response = client.get("/boards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []

def test_get_boards_one_saved(client, one_board):
    # Act
    response = client.get("/boards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body[0]["id"] == BOARD_ID
    assert response_body[0]["title"] == TITLE
    assert response_body[0]["owner"] == OWNER

def test_get_board_by_id(client, one_board):
    # Act
    response = client.get("/boards/1")
    response_body = response.get_json()

    # Assert
    assert response_body["id"] == BOARD_ID
    assert response_body["title"] == TITLE
    assert response_body["owner"] == OWNER

def test_get_board_by_id_not_found(client):
    # Act
    response = client.get("/boards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"message": "1 was not found"}

def test_get_invalid_board_id(client, one_board):
    # Act
    response = client.get("/boards/wrong")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400


#GET CARDS
def test_get_cards_per_board_one_saved(client, one_board, one_card):
    # Act
    response = client.get("/boards/1/cards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body[0]["id"] == CARD_ID
    assert response_body[0]["message"] == MESSAGE
    assert response_body[0]["likes_count"] == LIKES_COUNT

#do I need to do this test because it's a new endpoint or can the existing test above check this????
def test_get_cards_board_not_found(client):
    # Act
    response = client.get("/boards/1/cards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"message": "1 was not found"}

def test_get_cards_none_saved_to_board(client, one_board):
    # Act
    response = client.get("/boards/1/cards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []


# POST BOARDS
def test_create_board(client):
    # Act
    response = client.post("/boards", json={
        "title": TITLE,
        "owner": OWNER
    })

    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body["id"] == BOARD_ID

    new_board = Board.query.get(1)
    assert new_board
    assert new_board.title == TITLE
    assert new_board.owner == OWNER

def test_create_board_has_title(client):
    # Act
    response = client.post("/boards", json={
        "owner": OWNER
    })
    response_body = response.get_json()

    # Assert
    assert "details" in response_body
    assert "Request body must include name." in response_body["details"]
    assert response.status_code == 400
    assert Board.query.all() == []

def test_create_board_has_owner(client):
    # Act
    response = client.post("/boards", json={
        "title": TITLE
    })
    response_body = response.get_json()

    # Assert
    assert "details" in response_body
    assert "Request body must include owner." in response_body["details"]
    assert response.status_code == 400
    assert Board.query.all() == []


#POST CARDS
def test_create_card(client, one_board):
    # Act
    response = client.post("/boards/1/cards", json={
        "message": MESSAGE,
    })

    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body["id"] == CARD_ID

    new_card = Card.query.get(1)
    assert new_card
    assert new_card.message == MESSAGE

def test_create_card_has_message(client, one_board):
    # Act
    response = client.post("/boards/1/cards", json={})
    response_body = response.get_json()

    # Assert
    assert response_body == {"details": "Request body must include message."}
    assert response.status_code == 400
    # assert "details" in response_body
    # assert "Request body must include message." in response_body["details"]
    # assert response.status_code == 400
    assert Card.query.all() == []
