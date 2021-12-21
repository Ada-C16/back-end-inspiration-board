import pytest
from app import create_app
from app.models.board import Board
from app.models.card import Card
from app import db
from flask.signals import request_finished

BOARD_TITLE = "A New Board"
BOARD_OWNER = "Some Name"

@pytest.fixture
def app():
    app = create_app({"TESTING": True})

    # @request_finished.connect_via(app)
    # def expire_session(sender, response, **extra):
    #     db.session.remove()

    with app.app_context():
        db.create_all()
        yield app

    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def one_board(app):
    new_board = Board(
        title=BOARD_TITLE, 
        owner=BOARD_OWNER,
        )
    db.session.add(new_board)
    db.session.commit()