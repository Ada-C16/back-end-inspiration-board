import pytest
from app import create_app
from app.models.board import Board
from app.models.card import Card
from app import db


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
def one_board(app):
    new_board = Board(
        title="XOXO", owner="Someone")
    db.session.add(new_board)
    db.session.commit()


@pytest.fixture
def two_boards(app):
    db.session.add_all([
        Board(
        title="Love", owner="Someone"),
        Board(
        title="XOXO", owner="Someone else")
    ])
    db.session.commit()


@pytest.fixture
def one_card(app):
    new_card = Card(message="You are very special!")
    db.session.add(new_card)
    db.session.commit()


@pytest.fixture
def one_card_belongs_to_one_board(app, one_board, one_card):
    board = Board.query.first()
    card = Card.query.first()
    board.tasks.append(card)
    db.session.commit()