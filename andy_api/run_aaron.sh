#!/bin/bash

# Only change the values enclosed in the dashes
# ---------------------------------------------------------------------------- #
# Change this to the absolute path of the service key for Google Cloud
ABSOLUTE_PATH_TO_KEY="C:\Users\Legacy\Desktop\service_key_file.json"
# Change this to the name of the stockfish file
# NOTE: this file should be placed in andy_api/stockfish_engine
STOCKFISH_NAME="stockfish"
# NOTE: you may have to change the slashes if you are in windows
STOCKFISH_BASE_DIR=".\stockfish_engine"
STOCKFISH_LOCATION="$STOCKFISH_BASE_DIR\$STOCKFISH_NAME"
# Set this to the "mode" you want to run the application in. This will affect
# where logs are saved and which base script is run.
#
# Should be one of: "development" | "demo"
APP_MODE="development"
# ---------------------------------------------------------------------------- #

SCRIPT_NAME="run_base.sh"

# Run the app
exec sh $SCRIPT_NAME $APP_MODE $ABSOLUTE_PATH_TO_KEY $STOCKFISH_LOCATION
