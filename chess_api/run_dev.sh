#!/bin/bash

# Set flask environment variables
export FLASK_APP=chess_api
export FLASK_ENV=development

# Run the app
exec flask run -p 5001