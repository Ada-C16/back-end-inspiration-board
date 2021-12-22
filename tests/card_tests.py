from app.models.card import Card

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
    assert response_body == "card deleted"
    assert response.status_code == 200
    assert Card.query.all() == []

def test_delete_card_not_found(client, one_board):
    # Act
    response = client.delete("/cards/1")
    response_body = response.get_json()

    # Assert
    assert response_body == {"Card {card.card_id} was not found"}
    assert response.status_code == 404
    assert Card.query.all() == []