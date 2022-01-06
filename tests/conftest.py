import pytest
from app import create_app
from app import db
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

@pytest.fixture
def one_card(app):
    new_card = Card(
        message="Keep doing YOU, boo", likes_count=0)
    db.session.add(new_card)
    db.session.commit()