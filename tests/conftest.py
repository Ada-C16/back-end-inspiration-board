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


# This fixture gets called in every test that references "one_board".
# This fixture creates a board and saves it in the database.
@pytest.fixture
def one_board(app):
    new_board = Board(
        owner_name="Ansel", title="Sloth board")
    db.session.add(new_board)
    db.session.commit()


# This fixture gets called in every test that references "three_boards".
# This fixture creates three boardes and saves them in the database. 
@pytest.fixture
def three_boards(app):
    db.session.add_all([
        Board(
            owner_name="Piglet", title="Nice notes 🌷"),
        Board(
            owner_name="Pooh", title="Best spots to find honey"),
        Board(
            owner_name="Eeyore", title="Sadboi board 😭")
    ])
    db.session.commit()


# This fixture gets called in every test that references "one_card".
# This fixture creates a card and saves it in the database. 
@pytest.fixture
def one_card(app, one_board):
    new_card = Card(
        message="This is our last project before Capstone!", 
        likes_count=0,
        board_id=1
        )
    db.session.add(new_card)
    db.session.commit()
