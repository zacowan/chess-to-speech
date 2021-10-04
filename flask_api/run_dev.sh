#!/bin/bash

# Change this to the proper path
ABSOLUTE_PATH_TO_KEY="/Users/zacowan/development/chess-to-speech/flask_api/service_key_file.json"

# Set path to service account key
export GOOGLE_APPLICATION_CREDENTIALS=$ABSOLUTE_PATH_TO_KEY

# Set flask environment variables
export FLASK_APP=api
export FLASK_ENV=development

# Run the app
exec flask run
