from app.models.card import Card
from app.models.board import Board

# BOARD
def test_get_boards_no_boards_in_database(client):
    response = client.get("/boards")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == []

# CARD
def test_get_cards_no_cards_in_database(client):
    response= client.get("/cards")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == []

# BOARD
def test_get_boards_one_board_saved(client, one_board):
    response = client.get('/boards/1')
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body == [
        {
            "id":1,
            "title":"XOXO", 
            "owner":"Someone", 
            "cards":[]  
        }
    ]

#CARD
def test_get_cards_one_card_saved(client, one_card):
    response = client.get('/boards/one_board')
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body == [
        {
            "id":1,
            "title":"XOXO", 
            "owner":"Someone",    
        }
    ]
