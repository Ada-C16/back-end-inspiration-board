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

def test_delete_card(client, one_card):
    # Act
    response = client.delete("/cards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {
        'details': f'Card 1 succesfully deleted'
    }
    assert Card.query.get(1) == None


def test_delete_card_not_found(client):
    # Act
    response = client.delete("/cards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {'message' : 'Card 1 was not found'}
    assert Card.query.all() == []

def test_create_card(client):
    # Act
    response = client.post("/cards", json={
        "message": "Test message",
        "likes_count": 8
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body == {
        "message": "Test message",
        "likes_count": 8
    }
    new_card = Card.query.get(1)
    assert new_card 
    assert new_card.message == "Test message"
    assert new_card.likes_count == 8
   

def test_create_card_must_contain_message(client):
    # Act
    response = client.post("/cards", json={
        "likes_count": 8,
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert "details" in response_body
    assert response_body == {
        "details" : "Invalid request body"
    }
    assert Card.query.all() == []

def test_create_card_must_contain_likes_count(client):
    # Act
    response = client.post("/cards", json={
        "message": "Test message",
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert "details" in response_body
    assert response_body == {
        "details" : "Invalid request body"
    }
    assert Card.query.all() == []

def test_get_boards_no_saved_boards(client):
    # Act
    response = client.get("/boards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []

def test_get_boards_one_saved_board(client, one_board):
    # Act
    response = client.get("/boards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body == [
        {
            "id" : 1,
            "title" : "Test Board",
            "owner" : "Sandra"
        }
    ]
def test_get_board(client, one_board):
    # Act
    response = client.get("/boards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "board" in response_body
    assert response_body == {
         {
            "id" : 1,
            "title" : "Test Board",
            "owner" : "Sandra"
        }
    }

def test_board_not_found(client):
    # Act
    response = client.get("/board/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {'message': 'Board 1 was not found'}