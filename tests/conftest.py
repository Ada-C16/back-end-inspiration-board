import pytest
from app import create_app
from app import db
from app.models.board import Board
from app.models.card import Card


@pytest.fixture
def app():
    # create the app with a test config dictionary
    app = create_app({"TESTING": True})

    with app.app_context():
        db.create_all()
        yield app

    # close and remove the temporary database
    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


# This fixture creates a board and saves it in the database
# @pytest.fixture
# def one_board(app):
#     new_board = Board(
#         title="C16 Inspiration board", owner="Ada lovelace"
#     )
#     db.session.add(new_board)
#     db.session.commit()

