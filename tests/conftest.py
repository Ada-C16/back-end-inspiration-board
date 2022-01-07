import pytest
from app import create_app
from app import db
from app.models.board import Board
from app.models.card import Card
from flask.signals import request_finished

BOARD_ID = 1
TITLE = "Test Board"
OWNER = "Test Group"

CARD_ID = 1
MESSAGE = "Test message"
LIKES_COUNT = 3


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

@pytest.fixture
def one_card(app):
    new_card = Card(
        message=MESSAGE,
        board_id=BOARD_ID
    )
    db.session.add(new_card)
    db.session.commit()

@pytest.fixture
def one_board(app):
    new_board = Board(
        owner=OWNER,
        title=TITLE
    )
    db.session.add(new_board)
    db.session.commit()