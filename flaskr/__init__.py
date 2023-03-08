import os

from flask import Flask

from . import auth
from . import db
from flask_sqlalchemy import SQLAlchemy


def create_app(test_config=None):
    # Create and config the app.
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY='dev', DATABASE=os.path.join(
        app.instance_path, 'flaskr.sqlite'))

   # Ensure the instance folder exists.
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Register auth related routes.
    app.register_blueprint(auth.bp)

    # Hook up the database to the app.
    db.init_app(app)

    return app
