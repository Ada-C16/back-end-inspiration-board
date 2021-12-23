from flask import Blueprint, request, jsonify, make_response
from app import db

board_bp = Blueprint('board', __name__, url_prefix="/board")