from flask import (
    Blueprint, request, jsonify
)
from . import chess_logic

bp = Blueprint('chess_api', __name__, url_prefix='/chess_api')

@bp.route("/start-game", methods=["POST"])
def start_game():
    if request.method == "POST":
        chess_logic.start_game()
        try:
            return "Chess engine set and board cleared."
        except:
            return "Could not determine intent"

@bp.route("/get-best-move", methods=["GET"])
def get_best_move():
    if request.method == "GET":
        best_move = chess_logic.get_best_move()

        try:
            return jsonify(best_move)
        except:
            return "Could not determine intent"

@bp.route("/get-current-player", methods=["GET"])
def get_current_player():
    if request.method == "GET":
        current_player = chess_logic.get_current_player()

        try:
            return jsonify(current_player)
        except:
            return "Could not determine intent"

@bp.route("/move-piece", methods=["POST"])
def move_piece():
    if request.method == "POST":
        from_pos = request.args.get('from_pos')
        to_pos = request.args.get('to_pos')
        move_sequence = request.args.get('move_sequence')

        if (from_pos == None or to_pos == None) and move_sequence == None:
            return "Insuffient arguments provided."
        if from_pos != None and to_pos != None and move_sequence != None:
            return "Too many arguments provided."
        if from_pos != None and to_pos != None:
            response = chess_logic.move_piece(from_pos, to_pos)
        else:
            response = chess_logic.move_piece(move_sequence)

        try:
            return jsonify(response)
        except:
            return "Could not determine intent"