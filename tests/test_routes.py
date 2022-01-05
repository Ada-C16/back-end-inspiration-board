from app.models.board import Board
from app.models.card import Card 

def test_get_board_no_saved_boards(client):
    # Act
    response = client.get("/boards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []


def test_get_boards_one_saved_board(client, one_board):
    # Act
    response = client.get("/boards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {
            "id": 1,
            "owner_name": "Ansel",
            "title": "Sloth board"
        }


def test_get_boards_three_saved_boards(client, three_boards):
    # Act
    response = client.get("/boards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body[0]['id'] == 1
    assert response_body[1]['id'] == 2
    assert response_body[2]['id'] == 3
    assert response_body[0] == {
            'id': 1, 
            'owner_name': 'Piglet', 
            'title': 'Nice notes 🌷'
        }


def test_create_board(client):
    # Act
    response = client.post("/boards", json={
        "owner_name": "Example owner",
        "title": "Example title"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    new_board = Board.query.get(1)
    assert new_board
    assert new_board.owner_name == "Example owner"
    assert new_board.title == "Example title"


def test_delete_board(client, three_boards):
    # Act
    response = client.delete("/boards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {
        'id': 1, 
        'owner_name': 'Piglet', 
        'title': 'Nice notes 🌷'
    }
    assert len(Board.query.all()) == 2 


def test_get_cards_no_saved_cards(client):
    # Act
    response = client.get("/boards/1/cards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []


def test_add_one_card_and_get_one_card(client, one_board):
    # Act - add one card
    card_response = client.post("/boards/1/cards", json={
        "board_id" : "1", 
        "message" : "Example message--hello world!", 
        "likes_count" : "0"
    })

    # Act - get one card
    board_response = client.get("/boards/1/cards")
    board_response_body = board_response.get_json()

    # Assert
    assert card_response.status_code == 200
    assert board_response.status_code == 200
    assert len(board_response_body) == 1
    assert board_response_body == [{
            'board_id': 1, 
            'id': 1, 
            'likes_count': 0, 
            'message': 'Example message--hello world!'
        }]


def test_add_two_cards_and_get_two_cards(client, one_board):
    # Act - add two cards
    card_response = client.post("/boards/1/cards", json={
        "board_id" : "1", 
        "message" : "A message", 
        "likes_count" : "0"
    })

    second_card_response = client.post("/boards/1/cards", json={
        "board_id" : "1", 
        "message" : "Another message", 
        "likes_count" : "0"
    })

    # Act - get two cards
    board_response = client.get("/boards/1/cards")
    board_response_body = board_response.get_json()

    # Assert
    assert card_response.status_code == 200
    assert second_card_response.status_code == 200
    assert board_response.status_code == 200
    assert len(board_response_body) == 2
    assert board_response_body == [
            {
                'board_id': 1, 
                'id': 1, 
                'likes_count': 0, 
                'message': 'A message'
            }, 
            {
                'board_id': 1, 
                'id': 2, 
                'likes_count': 0, 
                'message': 'Another message'
            }
        ]


def test_delete_card(client, one_card):
    # Act
    response = client.delete("/cards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {
            'board_id': 1, 
            'id': 1, 
            'likes_count': 0, 
            'message': 'This is our last project before Capstone!'
        }

    # Check that the card was deleted
    response = client.get("/cards/1")
    assert response.status_code == 404


def test_delete_card_not_found(client):
    # Act
    response = client.delete("/cards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == None
    assert Card.query.all() == []


# Need to be done by Rachael or Tiffany at some point 
def test_create_card_must_contain_message(client):
    pass 

