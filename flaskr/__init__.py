from flask import Flask

from . import auth


def create_app(test_config=None):
    # Create and config the app.
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY='dev')

    # Register auth related routes.
    app.register_blueprint(auth.bp)

    return app
