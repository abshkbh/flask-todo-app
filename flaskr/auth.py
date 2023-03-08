import functools

from flask import Blueprint, jsonify

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    return jsonify({'message': 'Got register request'})


@bp.route('/login', methods=('GET', 'POST'))
def login():
    return jsonify({'message': 'Got login request'})


@bp.route('/logout', methods=('GET', 'POST'))
def logout():
    return jsonify({'message': 'Got logout request'})
