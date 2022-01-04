from flask import Blueprint, jsonify, make_response, request, abort
from flask.helpers import make_response
from app.models.board import Board
from app import db

board_bp = Blueprint("board", __name__, url_prefix="/boards")