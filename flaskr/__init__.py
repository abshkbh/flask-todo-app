import os
import sqlite3

from flask import Flask
from flaskr.error import bad_request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

# Needs to be initialized before all users of "db".
db = SQLAlchemy()

from flaskr import auth
from flaskr import location

def create_local_db_if_not_present(app, dbase):
    """
        Creates a local SQLite3 DB file if it's not present.
    """

    # Create DB if not already present.
    if not os.path.isfile(os.path.join(app.instance_path, app.config['DB_FILE_NAME'])):
        with app.app_context():
            print("Creating new DB")
            dbase.create_all()


def create_app():
    """
        Creates an app instance. We assume an "instance" folder already exists.
    """

    # Create and config the app.
    app = Flask(__name__, instance_relative_config=True)

    # We always require a config file to run.
    if not app.config.from_pyfile('config.py'):
        raise FileNotFoundError()

    # Hook up the database to the app. This will be used for ORMs.
    db.init_app(app)

    # Set up JWT based token management.
    #
    # TODO: Figure out if this should be initialized here or in location.py or in a separate module
    # altogether.
    jwt = JWTManager(app)

    if app.config['USE_LOCAL_DB']:
        create_local_db_if_not_present(app, db)

    # Register error handlers across blueprints.
    app.register_error_handler(400, bad_request)

    # Register auth related routes.
    app.register_blueprint(auth.bp)

    # Register location related routes.
    app.register_blueprint(location.bp)

    return app
