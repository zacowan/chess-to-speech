#!/bin/bash

# Args
# The starting board to return, should be one of: "full" | "demo"
# "full" by default
BOARD=${1:-full}

# Only change the values enclosed in the dashes
# ---------------------------------------------------------------------------- #
# Change this to the absolute path of the service key for Google Cloud
ABSOLUTE_PATH_TO_KEY="C:\Users\selen\Desktop\ChessToSpeech\chess-to-speech\andy_api\service_key_file.json"
# Change this to the name of the stockfish file
# NOTE: this file should be placed in andy_api/stockfish_engine
STOCKFISH_NAME="stockfish.exe"
# Set this to the "mode" you want to run the application in. This will affect
# where logs are saved and which base script is run.
#
# Suffix to append to the end of logs
# Should be one of: "development" | "demo1" | "demo2"
LOG_SUFFIX="demo2"
# ---------------------------------------------------------------------------- #
STOCKFISH_BASE_DIR="./stockfish_engine"
STOCKFISH_LOCATION="$STOCKFISH_BASE_DIR/$STOCKFISH_NAME"

SCRIPT_NAME="run_base.sh"

# Run the app
exec sh $SCRIPT_NAME $BOARD $LOG_SUFFIX $ABSOLUTE_PATH_TO_KEY $STOCKFISH_LOCATION
