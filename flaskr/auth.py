import functools

from .user import User
from . import db
from flask import Blueprint, jsonify, request, abort
from werkzeug.security import generate_password_hash

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=['POST'])
def register():
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
    return jsonify()


@bp.route('/logout', methods=['POST'])
def logout():
    return jsonify()
