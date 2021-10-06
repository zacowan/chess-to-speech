import chess
import chess.engine
import shelve

#Uppercase letters/pieces are white
#Lowercase letters/pieces are black
#the stockfish engine has uppercase/white going first

def start_game():
    engine = chess.engine.SimpleEngine.popen_uci("/usr/games/stockfish") #load stockfish as chess engine
    board=chess.Board() #initialize the board
    db = shelve.open("db")
    db["engine"] = engine
    db["board"] = board
    db.close()

def get_engine():
    db = shelve.open("db")
    engine = db.get("engine")
    db.close()
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
        return 1
    return 0

def move_piece(move_sequence):
    board = get_board()
    if(chess.Move.from_uci(move_sequence) in board.legal_moves): #check that move is legal
        board.push(chess.Move.from_uci(move_sequence)) #make move
        return 1
    return 0

