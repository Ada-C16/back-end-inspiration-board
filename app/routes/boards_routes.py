from flask import Blueprint, request, jsonify, make_response
from app.routes.cards_routes import *
from app import db

# example_bp = Blueprint('example_bp', __name__)

boards_bp = Blueprint("boards", __name__, url_prefix="/boards")


