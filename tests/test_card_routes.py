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

def test_create_card(client, one_board):
    response = client.post("/cards/1", json={"message": "@donutdadd"})
    response_body = response.get_json()

    assert response.status_code == 201
    assert "successful post" in response_body
    new_card = Card.query.first()
    assert new_card
    assert new_card.card_id == 1
    assert new_card.message == "@donutdadd"
    assert new_card.likes_count == 0

def test_create_card_failed(client, one_board):
    response = client.post("/cards/1", json={})
    response_body = response.get_json()

    assert response.status_code == 400
    assert "unsuccessful post" in response_body
    assert Card.query.all() == []

def test_update_card(client, one_card):
    response = client.put("/cards/1/like")
    response_body = response.get_json()

    assert response.status_code == 200
    assert "successful update" in response_body
    updated_card = Card.query.first()
    assert updated_card.card_id == 1
    assert updated_card.message == "@pukey.green"
    assert updated_card.likes_count == 1

def test_update_card_twice(client, one_card):
    client.put("/cards/1/like")
    response = client.put("/cards/1/like")
    response_body = response.get_json()

    assert response.status_code == 200
    assert "successful update" in response_body
    updated_card = Card.query.first()
    assert updated_card.card_id == 1
    assert updated_card.message == "@pukey.green"
    assert updated_card.likes_count == 2

def test_update_card_not_found(client):
    response = client.put("/cards/1/like")
    response_body = response.get_json()

    assert response.status_code == 404
    assert response_body == ''

def test_delete_card(client, one_card):
    response = client.delete("/cards/1")
    response_body = response.get_json()

    assert response.status_code == 200
    assert "successfully deleted @pukey.green" in response_body
    assert Card.query.get(1) == None

def test_delete_card_not_found(client):
    response = client.delete("/cards/1")
    response_body = response.get_json()

    assert response.status_code == 404
    assert response_body == ''
    assert Card.query.all() == []