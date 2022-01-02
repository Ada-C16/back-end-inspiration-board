from app.models.card import Card

def test_get_cards_no_saved_cards(client):
    # Act
    response = client.get("/cards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []


def test_get_cards_one_saved_cards(client, one_card):
    # Act
    response = client.get("/cards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body == [
        {
            "id": 1,
            "message":"Keep doing YOU, boo",
            "likes_count": 0
        }
    ]

def test_get_card(client, one_card):
    # Act
    response = client.get("/cards/1")
    response_body = response.get_json()
    
    # Assert
    assert response.status_code == 200
    assert response_body == [
        {
            "id": 1,
            "message":"Keep doing YOU, boo",
            "likes_count": 0
        }
    ]

def test_card_not_found(client):
    # Act
    response = client.get("/cards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {'message': 'Card 1 was not found'}
