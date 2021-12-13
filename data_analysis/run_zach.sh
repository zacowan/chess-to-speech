#!/bin/bash

# Set path to service account key
export GOOGLE_APPLICATION_CREDENTIALS="/Users/zacowan/development/chess-to-speech/andy_api/service_key_file.json"

# Run the app
exec python generate_csv.py
