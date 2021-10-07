import chess
import chess.engine
import shelve
import os

#Uppercase letters/pieces are white
#Lowercase letters/pieces are black
#the stockfish engine has uppercase/white going first

def initialize_board():
    board = chess.Board() #initialize the board
    board_storage = shelve.open("board_storage")
    board_storage["board"] = board
    board_storage.close()

def get_engine():
    dirname = os.path.dirname(__file__)
    engine_filename = dirname + "/UCI_engine/stockfish"
    engine = chess.engine.SimpleEngine.popen_uci(engine_filename) #load stockfish as chess engine
    return engine

def get_board():
    db = shelve.open("db")
    board = db.get("board")
    db.close()
    return board

def get_best_move():
    engine = get_engine()
    board = get_board()
    bestMove = engine.play(board, chess.engine.Limit(time=0.1)).move
    engine.close()
    return bestMove

def get_current_player():
    if chess.WHITE:
        return 'WHITE'
    return 'BLACK'

def move_piece(from_pos, to_pos):
    board = get_board()
    move_sequence = from_pos + to_pos
    if(chess.Move.from_uci(move_sequence) in board.legal_moves): #check that move is legal
        board.push(chess.Move.from_uci(move_sequence)) #make move
        return "Succesfully moved piece."
    return "Illegal move, please try again."

def move_piece(move_sequence):
    board = get_board()
    if(chess.Move.from_uci(move_sequence) in board.legal_moves): #check that move is legal
        board.push(chess.Move.from_uci(move_sequence)) #make move
        return "Succesfully moved piece."
    return "Illegal move, please try again."

