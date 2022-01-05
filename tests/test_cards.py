from app.models.card import Card
from flask import jsonify

BOARD_ID = 1
TITLE = "Test Board"
OWNER = "Test Group"

CARD_ID = 1
MESSAGE = "Test message"
LIKES_COUNT = 3

# test update likes count

# test delete


def test_delete_card(client, one_board, one_card):
    # Act
    response = client.delete("/cards/1")
    response_body = response.get_json()

    # Assert
    assert response_body == {"message": "card deleted"}
    assert response.status_code == 200
    assert Card.query.all() == []

def test_delete_card_not_found(client, one_board):
    # Act
    response=client.delete("/cards/1")
    response_body=response.get_json()
    print(response_body)
    # Assert
    assert response_body == {"message": "Card 1 was not found"}
    assert response.status_code == 404
    assert Card.query.all() == []

def test_add_like_to_card(client, one_board, one_card):
    # Act
    response = client.patch("/cards/1/like", json={})
    print(response)
    response_body=response.get_json()
    
    # Assert
    assert response_body["id"] == CARD_ID
    assert response_body["message"] == MESSAGE
    assert response_body["likes_count"] == 1
    # assert response_body == one_card.create_card_dict()
    assert response.status_code == 200

def test_add_like_to_card_not_found(client, one_board):
    # Act
    response = client.patch("/cards/1/like")
    response_body=response.get_json()
    
    # Assert
    assert response_body == {"message": "Card 1 was not found"}
    assert response.status_code == 404
    assert Card.query.all() == []

# def test_add_like_to_card_missing_data(client, one_board, one_card):
#     # Act
#     response = client.patch("/cards/1/like")
#     response_body=response.get_json()
    
#     # Assert
#     assert response_body == {"message": "Request body must include likes_count"}
#     assert response.status_code == 400