#!/bin/bash

# Change this to the proper path
# # For Bricson:
# ABSOLUTE_PATH_TO_KEY="C:\Users\selen\Desktop\ChessToSpeech\chess-to-speech\andy_api\service_key_file.json"
# For Zach:
ABSOLUTE_PATH_TO_KEY="/home/natestull/Documents/School/CIS4930 - Special Topics in CISE: Spoken Dialogue Systems/Project/develop/chess-to-speech/andy_api/api/service_key_file.json"

# Set path to service account key
export GOOGLE_APPLICATION_CREDENTIALS=$ABSOLUTE_PATH_TO_KEY

# Set flask environment variables
export FLASK_APP=api
export FLASK_ENV=development
export DEMO_MODE=True

# Set the application environment variables
export LOGGING_SUFFIX=development

# Run the app
exec flask run
