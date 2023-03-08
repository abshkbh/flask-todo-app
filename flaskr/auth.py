import functools

from flask import Blueprint, jsonify

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    return jsonify({'message': 'Got register request'})
