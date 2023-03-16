from flaskr.schema import AppUser
from flaskr import db
from flask import Blueprint, jsonify, request, abort
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required

bp = Blueprint('auth', __name__, url_prefix='/auth')


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

    user = AppUser(username=username,
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

    user = AppUser.query.filter_by(username=username).first()
    if not user:
        error_string = "user {} not found".format(username)
        abort(400, {'error': error_string})

    if not check_password_hash(user.password_hash, password):
        error_string = "user {}'s password don't match".format(username)
        abort(400, {'error': error_string})

    # Create the cookie that would be used to identify the logged in user.
    access_token = create_access_token(identity=user.id)

    return jsonify({'access_token': access_token})


@bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """Logout a logged in user."""
    # TOODO: Clear jwt.
    return jsonify()
