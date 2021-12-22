from operator import contains
from app.models.board import Board
from app.models.card import Card

BOARD_TITLE = "A New Board"
BOARD_OWNER = "Some Name"

def test_create_new_board(client):
    # Act
    response = client.post("/boards", json = {
        "title": BOARD_TITLE,
        "owner": BOARD_OWNER
    })

    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body["title"] == BOARD_TITLE
    assert response_body["owner"] == BOARD_OWNER

    new_board = Board.query.get(1)

    assert new_board
    assert new_board.title == BOARD_TITLE

def test_create_board_must_contain_title_and_owner(client):
    # Act
    response = client.post("/boards", json={
        "title": "",
        "owner": ""
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {
        "details": "Request body must include title and owner."
    }
    assert Board.query.all() == []

def test_create_board_must_contain_title(client):
    # Act
    response = client.post("/boards", json={
        "title": "",
        "owner": BOARD_OWNER
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {
        "details": "Request body must include title."
    }
    assert Board.query.all() == []

def test_create_board_must_contain_owner(client):
    # Act
    response = client.post("/boards", json={
        "title": BOARD_TITLE,
        "owner": ""
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {
        "details": "Request body must include owner."
    }
    assert Board.query.all() == []

def test_get_boards_one_saved_board(client, one_board):
    # Act
    response = client.get("/boards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body == [
        {
            "board_id": 1,
            "title": "A New Board",
            "owner": "Some Name"
        }]

def test_get_empty_list_no_saved_boards(client):
    # Act
    response = client.get("/boards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 0
    assert response_body == []

def test_three_saved_boards(client, three_boards):
    # Act
    response = client.get("/boards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body == [
        {
            "board_id": 1,
            "title": "A New Board",
            "owner": "Some Name"
        },
        {
            "board_id": 2,
            "title": "Second Board",
            "owner": "Second Name"
        },
        {
            "board_id": 3,
            "title": "Third Board",
            "owner": "Third Name"
        }
    ]

def test_get_one_board(client, one_board):
    # Act
    response = client.get("/boards/1")
    response_body = response.get_json()

    # Assert
    assert response_body["board_id"] == 1
    assert response_body["title"] == BOARD_TITLE
    assert response_body["owner"] == BOARD_OWNER

def test_invalid_board_id(client):
    # Act
    response = client.get("/boards/test")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {
        "message": "Board id needs to be an integer"}

def test_board_not_found(client):
    # Act
    response = client.get("/boards/3")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {
        "message": "Board 3 was not found"}

# def test_create_new_card(client):

# def test_get_cards_one_card(client, one_card):

# def test_get_cards_three_cards(client, three_cards):

# def test_get_no_cards_returns_empty_array(client, one):