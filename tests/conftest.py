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

@pytest.fixture
def three_boards(app):
    db.session.add_all([
    Board(
        title=BOARD_TITLE,
        owner=BOARD_OWNER
    ),

    Board(
        title = "Second Board",
        owner = "Second Name"
    ),
    Board(
        title = "Third Board",
        owner = "Third Name"
    )
    ])

    db.session.commit()

@pytest.fixture
def one_card(app):
    new_card = Card(message = "This is a new card!",)
    db.session.add(new_card)
    db.session.commit()

@pytest.fixture
def three_cards(app):
    db.session.add_all([
        Card(message = "This is a new card!"),
        Card(message = "Second card"),
        Card(message = "Third card")
    ])
    db.session.commit()

@pytest.fixture
def one_card_belongs_to_one_board(app, one_board, one_card):
    card = Card.query.first()
    board = Board.query.first()
    board.cards.append(card)
    db.session.commit()

@pytest.fixture
def three_cards_belong_to_one_board(app, one_board, three_cards):
    cards = Card.query.all()
    board = Board.query.first()
    board.cards.append(cards)
    db.session.commit()