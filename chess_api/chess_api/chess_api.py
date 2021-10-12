from flask import (
    Blueprint, request, jsonify
)
from . import chess_logic
import json

bp = Blueprint('chess_api', __name__, url_prefix='/chess_api')

@bp.route("/start-game", methods=["POST"])
def initialize_board():
    if request.method == "POST":
        try:
            chess_logic.initialize_board()
            json_str = '{"description": "Chess engine set and board cleared."}'
            json_obj = json.load(json_str)
            return json_obj
        except:
            json_str = '{"description": "Could not determine intent"}'
            json_obj = json.load(json_str)
            return json_obj

@bp.route("/get-best-move", methods=["GET"])
def get_best_move():
    if request.method == "GET":
        best_move = chess_logic.get_best_move()
        json_str = '{"best_move": "'+best_move+'"}'
        json_obj = json.load(json_str)
        return json_obj

@bp.route("/get-current-player", methods=["GET"])
def get_current_player():
    if request.method == "GET":
        current_player = chess_logic.get_current_player()
        json_str = '{"current_player": "'+current_player+'"}'
        json_obj = json.load(json_str)
        return json_obj

@bp.route("/move-piece", methods=["POST"])
def move_piece():
    if request.method == "POST":
        from_pos = request.args.get('from_pos')
        to_pos = request.args.get('to_pos')
        move_sequence = request.args.get('move_sequence')
        try:
            if (from_pos == None or to_pos == None) and move_sequence == None:
                json_str = '{"description": "Insuffient arguments provided."}'
            if from_pos != None and to_pos != None and move_sequence != None:
                json_str = '{"description": "Too many arguments provided."}'
            if from_pos != None and to_pos != None:
                json_str = '{description": "'+chess_logic.move_piece(from_pos, to_pos)+'"}'
            else:
                json_str = '{"description": "'+chess_logic.move_piece(move_sequence)+'"}'
            json_obj = json.load(json_str)
            return json_obj
        except:
            json_str = '{"description": "Could not determine intent"}'
            json_obj = json.load(json_str)
            return json_obj