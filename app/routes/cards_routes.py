from flask import Blueprint, request, jsonify, make_response
from app.routes.boards_routes import *
from app import db

# example_bp = Blueprint('example_bp', __name__)


cards_bp = Blueprint("cards", __name__, url_prefix="/cards")

