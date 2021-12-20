from app.models.card import Card

def test_get_cards_no_saved_cards(client):
    response= client.get("/cards")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == []

def test_get_cards_one_saved_card(client, one_card):
    response= client.get("/cards")
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body == [
        {
            "id": 1,
            "message": "@pukey.green",
            "likes_count": 0
        }
    ]

