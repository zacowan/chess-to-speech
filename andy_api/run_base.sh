#!/bin/bash

# Command-line args
STARTING_BOARD=$1
LOG_SUFFIX=$2
KEY_PATH=$3
STOCKFISH_LOCATION=$4

# Set path to service account key
export GOOGLE_APPLICATION_CREDENTIALS=$KEY_PATH

# Set the stockfish location
export STOCKFISH_LOCATION=$STOCKFISH_LOCATION

# Set flask environment variables
export FLASK_APP=api
export FLASK_ENV=development

# Set the app mode
export STARTING_BOARD=$STARTING_BOARD

# Set the application environment variables
export LOGGING_SUFFIX=$LOG_SUFFIX

# Run the app
exec python -m flask run
