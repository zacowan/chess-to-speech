#!/bin/bash

# Change this to the proper path
ABSOLUTE_PATH_TO_KEY="/Users/zacowan/development/chess-to-speech/flask_api/service_key_file.json"

export GOOGLE_APPLICATION_CREDENTIALS=$ABSOLUTE_PATH_TO_KEY
cd src/
exec flask run
