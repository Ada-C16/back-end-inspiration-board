from flask.wrappers import Response
from app.models.board import Board

### CREATE TESTS: /boards ENDPOINT ###
def test_create_board(client):
    # Act
    response = client.post("/boards", json={
        "title": "Fancy new board",
        "owner": "Pine Prez"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body == {
            "board_id": 1,
            "title": "Fancy new board",
            "owner": "Pine Prez"
    }

def test_create_board_no_title(client):
    # Act
    response = client.post("/boards", json={
        "owner": "Pine Prez"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert "error" in response_body
    assert response_body == {
        "error": "User must include title."
    }
    assert Board.query.all() == []

def test_create_board_no_owner(client):
    # Act
    response = client.post("/boards", json={
        "title": "Fancy new board"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert "error" in response_body
    assert response_body == {
        "error": "User must include owner."
    }
    assert Board.query.all() == []



### READ TESTS: /boards ENDPOINT ###
def test_get_boards_no_saved_boards(client):
    # Act
    response = client.get("/boards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []

def test_get_one_saved_board(client, one_board):
    # Act
    response = client.get("/boards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body == [
        {
            "board_id": 1,
            "title": "Really extra festive",
            "owner": "Mariah Carey"
        }
    ]

def test_get_three_saved_boards(client, three_boards):
    # Act
    response = client.get("/boards")
    response_body = response.get_json()

    # Assert 
    assert response.status_code == 200 
    assert len(response_body)  == 3
    assert response_body == [
        {
            "board_id": 1,
            "title": "Bodies of water in which to skinny dip",
            "owner": "Ariel"
            },
            {
            "board_id": 2,
            "title": "Rare plants I aspire to own",
            "owner": "Anthurium"
            }, {
            "board_id": 3,
            "title": "Luxury items to buy with my tech money",
            "owner": "Anya"
            } 
    ]



### DELETE TEST: /boards ENDPOINT ###
def test_delete_one_board_from_one_saved_board(client, one_board):
    # Act
    response = client.delete("/boards/1")
    response_body = response.get_json()
    check_for_deletion = client.get("/boards")
    check_response_body = check_for_deletion.get_json()

    # Assert
    assert response.status_code == 200
    assert len(check_response_body) == 0
    assert check_response_body == []

def test_delete_one_board_from_three_saved_boards(client, three_boards):
    # Act
    response = client.delete("/boards/3")
    response_body = response.get_json()
    check_for_deletion = client.get("/boards")
    check_response_body = check_for_deletion.get_json()

    # Assert
    assert response.status_code == 200
    assert len(check_response_body) == 2
    assert response_body == {
        "message": f"Board 3 was successfully deleted"
    }