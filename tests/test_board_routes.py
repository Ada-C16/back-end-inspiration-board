from app.models.board import Board

def test_get_boards_no_saved_boards(client):
    response= client.get("/boards")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == []

def test_get_boards_one_saved_board(client, one_board):
    response= client.get("/boards")
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body == [['Cool Artists on Instagram',1]]

def test_create_board(client):
    response = client.post("/boards", json={"title": 'Food Board', "owner": 'Juliana'})
    response_body = response.get_json()

    assert response.status_code == 201
    assert "Food Board" in response_body
    new_board = Board.query.first()
    assert new_board
    assert new_board.board_id == 1
    assert new_board.title == "Food Board"
    assert new_board.owner == 'Juliana'

def test_create_board_failed(client):
    response = client.post("/boards", json={})
    response_body = response.get_json()

    assert response.status_code == 400
    assert "unsuccessful post" in response_body
    assert Board.query.all() == []

def test_delete_board(client, one_board):
    response = client.delete("/boards/1")
    response_body = response.get_json()

    assert response.status_code == 200
    assert "successfully deleted Cool Artists on Instagram" in response_body
    assert Board.query.get(1) == None

def test_delete_board_not_found(client):
    response = client.delete("/boards/1")
    response_body = response.get_json()

    assert response.status_code == 404
    assert response_body == ''
    assert Board.query.all() == []

def test_get_one_card_from_one_board(client, one_card_belongs_to_one_board):
    response = client.get("/boards/1")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body["title"] == "Cool Artists on Instagram"
    assert response_body["owner"] == "Karishma"
    assert response_body["id"] == 1
    assert len(response_body["cards"]) == 1
    assert {
            "id": 1,
            "message": "@pukey.green",
            "likes_count": 0
            } in response_body["cards"]

def test_get_multiple_cards_from_one_board(client, multiple_cards_belong_to_one_board):
    response = client.get("/boards/1")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body["title"] == "Cool Artists on Instagram"
    assert response_body["owner"] == "Karishma"
    assert response_body["id"] == 1
    assert len(response_body["cards"]) == 4
    assert {
            "id": 1,
            "message": "@cairopaints",
            "likes_count": 0
    } in response_body["cards"]
    assert {
            "id": 2,
            "message": "@queerancestorsproject",
            "likes_count": 0
    } in response_body["cards"]
    assert {
            "id": 3,
            "message": "@rawlzzzart",
            "likes_count": 0
    } in response_body["cards"]
    assert {
            "id": 4,
            "message": "@smalldogbigwurld",
            "likes_count": 0
    } in response_body["cards"]

