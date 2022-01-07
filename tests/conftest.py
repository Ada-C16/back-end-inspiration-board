import pytest
from app import create_app
from app import db
from app.models.board import Board

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

# creates one board and saves it to the database
@pytest.fixture
def one_board(app):
    new_board = Board(title="Really extra festive",
                        owner="Mariah Carey")
    db.session.add(new_board)
    db.session.commit()

# creates three boards and saves them to the database
@pytest.fixture
def three_boards(app):
    db.session.add_all([
        Board(title="Bodies of water in which to skinny dip", owner="Ariel"),
        Board(title="Rare plants I aspire to own", owner="Anthurium"),
        Board(title="Luxury items to buy with my tech money", owner="Anya")
    ])
    db.session.commit()