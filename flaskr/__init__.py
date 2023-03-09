import os
import sqlite3

from flask import Flask

from . import auth
from flask_sqlalchemy import SQLAlchemy

# Needs to be declared before the app factory runs so that it could be linked with one instance of an app.
db = SQLAlchemy()


def create_app(test_config=None):
    # Create and config the app.
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY='dev', DB_FILE_NAME='flaskr.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
        app.config['DB_FILE_NAME']

   # Ensure the instance folder exists.
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Hook up the database to the app. This will be used for ORMs.
    db.init_app(app)

    # Create DB if not ready.
    if not os.path.isfile(os.path.join(app.instance_path, app.config['DB_FILE_NAME'])):
        with app.app_context():
            print("Creating new DB")
            db.create_all()

    # Register auth related routes.
    app.register_blueprint(auth.bp)

    return app
