from app import db
from app.models.board import Board
from flask import Blueprint, request, make_response, jsonify
import requests
import os

cards_bp = Blueprint("cards", __name__, url_prefix="/cards")

@cards_bp.route("", methods=["GET"])
def handle_cards():
    pass

@cards_bp.route("", methods=["POST"])
def post_card():
    pass

