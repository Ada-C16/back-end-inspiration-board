import pytest
from app.models.board import Board
from app.models.card import Card
from app import create_app
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
def one_card(app):
    new_card = Card(
        message = '@pukey.green'
    )
    db.session.add(new_card)
    db.session.commit()

@pytest.fixture
def four_cards(app):
    db.session.add_all([
        Card(
            message = '@cairopaints'),
        Card(
            message = '@queerancestorsproject'),
        Card(
            message = '@rawlzzzart'),
        Card(
            message = '@smalldogbigwurld')
    ])
    db.session.commit()


@pytest.fixture
def one_board(app):
    new_board = Board(
        title='Cool Artists on Instagram',
        owner='Karishma'
    )
    db.session.add(new_board)
    db.session.commit()

@pytest.fixture
def one_card_belongs_to_one_board(app, one_card, one_board):
    card = Card.query.first()
    board = Board.query.first()
    board.cards.append(card)
    db.session.commit()
