import functools

from flaskr.schema import User
from flaskr import db
from flask import Blueprint, jsonify, request, abort, session, g
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint('auth', __name__, url_prefix='/auth')


def login_required(view):
    """View decorator that redirects anonymous users to the login page."""

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            abort(400, {'error': 'login required'})

        return view(**kwargs)

    return wrapped_view


@bp.before_app_request
def load_logged_in_user():
    """If a user id is stored in the session, load the user object from
    the database into ``g.user``."""
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.filter_by(id=user_id).first()


@bp.route('/register', methods=['POST'])
def register():
    """Register a new user."""
    request_json = request.get_json()
    if not request_json:
        abort(400, {'error': 'no JSON data in the request'})

    username = request_json.get('username')
    if not username:
        abort(400, {'error': 'no username'})

    password = request_json.get('password')
    if not password:
        abort(400, {'error': 'no password'})

    user = User(username=username,
                password_hash=generate_password_hash(password))
    db.session.add(user)
    db.session.commit()
    return jsonify()


@bp.route('/login', methods=['POST'])
def login():
    """Login a user."""
    request_json = request.get_json()
    if not request_json:
        abort(400, {'error': 'no JSON data in the request'})

    username = request_json.get('username')
    if not username:
        abort(400, {'error': 'no username'})

    password = request_json.get('password')
    if not password:
        abort(400, {'error': 'no password'})

    user = User.query.filter_by(username=username).first()
    if not user:
        error_string = "user {} not found".format(username)
        abort(400, {'error': error_string})

    if not check_password_hash(user.password_hash, password):
        error_string = "user {}'s password don't match".format(username)
        abort(400, {'error': error_string})

    # Set cookie to login the browser.
    session.clear()
    session['user_id'] = user.id
    return jsonify()


@bp.route('/logout', methods=['POST'])
@login_required
def logout():
    """Logout a logged in user."""
    session.clear()
    return jsonify()
