#!/bin/bash

# Change this to the proper path
ABSOLUTE_PATH_TO_KEY="C:\Users\Legacy\Desktop\service_key_file.json"

# Set path to service account key
export GOOGLE_APPLICATION_CREDENTIALS=$ABSOLUTE_PATH_TO_KEY

# Set flask environment variables
export FLASK_APP=api
export FLASK_ENV=development

# Set the application environment variables
export LOGGING_SUFFIX=development

# Run the app
exec python -m flask run
