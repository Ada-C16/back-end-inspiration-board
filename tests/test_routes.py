from operator import contains
from app.models.board import Board
from app.models.card import Card

BOARD_TITLE = "A New Board"
BOARD_OWNER = "Some Name"

# This test doesn't work yet!
def test_create_new_board(client):
    # Act
    response = client.post("/boards", json = {
        "title": BOARD_TITLE,
        "owner": BOARD_OWNER
    })

    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body["title"] == BOARD_TITLE
    assert response_body["owner"] == BOARD_OWNER

    new_board = Board.query.get(1)

    assert new_board
    assert new_board.title == BOARD_TITLE