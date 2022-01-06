from app.models.board import Board

# Tests for GET requests (Board)
# def test_get_boards_no_saved_boards(client):
#     response = client.get("/boards")
#     response_body = response.get_json()

#     assert response.status_code == 200
#     assert response_body == []

# # Tests for POST requests (Board)
def test_create_board_must_contain_title(client):
    response = client.post("/boards", json={
        "owner": "test owner"
    })
    response_body = response.get_json()

    assert response.status_code == 400
    assert "details" in response_body
    assert response_body == {
        "details": "Invalid data"
    }
    assert Board.query.all() == []

def test_create_board_must_contain_owner(client):
    response = client.post("/boards", json={
        "title": "test title"
    })
    response_body = response.get_json()

    assert response.status_code == 400
    assert "details" in response_body
    assert response_body == {
        "details": "Invalid data"
    }
    assert Board.query.all() == []

def test_create_board_contains_all_requiremenets(client):
    response = client.post("/boards", json={
        "title": "test title",
        "owner": "test owner"
    })
    response_body = response.get_json()

    assert response.status_code == 201
    assert "board" in response_body
    assert response_body == {
        "board": {
            "id": 1,
            "title": "test title",
            "owner": "test owner"
        }
    }
    new_board = Board.query.get(1)
    assert new_board
    assert new_board.title == "test title"
    assert new_board.owner == "test owner"