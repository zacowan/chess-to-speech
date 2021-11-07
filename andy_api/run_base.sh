#!/bin/bash

# Command-line args
APP_MODE=$1
KEY_PATH=$2
STOCKFISH_LOCATION=$3

# Set path to service account key
export GOOGLE_APPLICATION_CREDENTIALS=$KEY_PATH

# Set the stockfish location
export STOCKFISH_LOCATION=$STOCKFISH_LOCATION

# Set flask environment variables
export FLASK_APP=api
export FLASK_ENV=development

# Set the app mode
export APP_MODE="demo"

# Set the application environment variables
export LOGGING_SUFFIX=$APP_MODE

# Run the app
exec python -m flask run
