#!/bin/bash

# Only change the values enclosed in the dashes
# ---------------------------------------------------------------------------- #
# Change this to the absolute path of the service key for Google Cloud
ABSOLUTE_PATH_TO_KEY="/home/natestull/Documents/School/CIS4930 - Special Topics in CISE: Spoken Dialogue Systems/Project/develop/chess-to-speech/andy_api/api/service_key_file.json"
# Change this to the name of the stockfish file
# NOTE: this file should be placed in andy_api/stockfish_engine
STOCKFISH_NAME="stockfish"
# Set this to the "mode" you want to run the application in. This will affect
# where logs are saved and which base script is run.
#
# Should be one of: "development" | "demo"
APP_MODE="development"
# ---------------------------------------------------------------------------- #
STOCKFISH_BASE_DIR="./stockfish_engine"
STOCKFISH_LOCATION="$STOCKFISH_BASE_DIR/$STOCKFISH_NAME"

SCRIPT_NAME="run_base.sh"

# Run the app
exec sh $SCRIPT_NAME $ABSOLUTE_PATH_TO_KEY $STOCKFISH_LOCATION

