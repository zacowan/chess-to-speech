"""Initialization of flask app.

This module serves the purpose of initializing the flask application.

"""
from pathlib import Path
from flask import Flask
from flask_cors import CORS
from . import api_routes
from .state_manager import SHELVE_DIRECTORY


def create_app(test_config=None):
    # Create shelve directory
    Path(SHELVE_DIRECTORY).mkdir(parents=True, exist_ok=True)
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    CORS(app, resources={r"/*": {"origins": "*"}})
    app.config.from_mapping(
        SECRET_KEY="dev",
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # Display the routes available
    @app.route("/")
    def health_check():
        return "Successfully running api!"

    # Register the API blueprint
    app.register_blueprint(api_routes.bp)

    return app
