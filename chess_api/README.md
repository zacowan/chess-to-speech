## Getting Python Set Up

1. Make sure you have Python version 3.9 installed.
2. Install pipenv by following the instructions (here)[https://pipenv.pypa.io/en/latest/install/#pragmatic-installation-of-pipenv].
3. Inside of the project directory, run pipenv install. This will install the required packages specified in Pipfile.

## Starting Chess API

Run `chmod +x run_dev.sh` to get the right privledges for using a script to run the app. Then, top level chess_api folder, run "./run_dev.sh"

## Endpoints

1. `http://localhost:5001/start-game` (POST)

Initializes and stores a board object in a persistant Shelve databse. Returns a string indicating if the action was succesful or not. This endpoint must be called before the beginning of every game to ensure the board is reset.

2. `http://localhost:5001/get-best-move` (GET)

Returns a 4 character string indicating the best possible move for the player whose turn it currently is. The first two characters indicate the column and row (in that order) the piece is currently at. The last two characters indicate the column and row (in that order) that the piece should be moved to.

3. `http://localhost:5001/get-current-player` (GET)

Returns a string- "WHITE" or "BLACK", depending on the current player. It's important to note that white always moves first.

3. `http://localhost:5001/move-piece` (POST)

Moves a piece to a destination specified in the API request. The request can either take both "from_pos" and "to_pos" or only "move_sequence" as arguments. "from_pos" is a two character string with the column and row (in that order) of the current location of the piece to be moved. "to_pos" is a two character string with the column and row (in that order) of the destination of the piece to be moved. If a user opts to provide only the "move_sequence" argument instead, they provide "from_pos" + "to_pos" as one joined 4 character string.