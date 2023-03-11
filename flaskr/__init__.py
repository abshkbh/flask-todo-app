import os
import sqlite3

from flask import Flask
from flaskr.error import bad_request
from flask_sqlalchemy import SQLAlchemy

# Needs to be initialized before all users of "db".
db = SQLAlchemy()

from flaskr import todos
from flaskr import auth

def create_app(test_config=None):
    # Create and config the app.
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY='dev', DB_FILE_NAME='flaskr.db')
    # Note URL should start with postgresql:// vs postgres://.
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://johndoe65535:ZleLGaC6pIDMQ40BgDYtG1YgRd2eYXEh@dpg-cg5sfkl269v5l63v3meg-a.oregon-postgres.render.com/maverick_flask_todo_db'

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

    # Register error handlers across blueprints.
    app.register_error_handler(400, bad_request)

    # Register auth related routes.
    app.register_blueprint(auth.bp)

    # Register todos related routes.
    app.register_blueprint(todos.bp)

    return app
