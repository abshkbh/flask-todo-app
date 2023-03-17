from flaskr.schema import AppUser
from flaskr import db
from flask import Blueprint, jsonify, request, abort
from flask_jwt_extended import jwt_required, get_jwt_identity

bp = Blueprint('location', __name__, url_prefix='/update')


@bp.route('/update', methods=['POST'])
@jwt_required()
def update():
    """Update the location of a user"""
    request_json = request.get_json()
    if not request_json:
        abort(400, {'error': 'no JSON data in the request'})

    coordinates = request_json['coordinates']
    if not coordinates:
        abort(400, {'error': 'no coordinates in the request'})

    current_user_id = get_jwt_identity()
    user = AppUser.query.filter_by(id=current_user_id).first()
    if not user:
        abort(400, {'error': 'user not found'})

    user.coordinates = coordinates
    db.session.commit()
    return jsonify()


@bp.route('/neighbors', methods=['GET'])
@jwt_required()
def neighbors():
    """Update the location of a user"""
    request_json = request.get_json()
    if not request_json:
        abort(400, {'error': 'no JSON data in the request'})

    # Filter other user's by the current user's coordinates.
    current_user_id = get_jwt_identity()
    users = AppUser.query.filter_by(
        coordinates=current_user_id.coordinates).all()
    neighbors_of_current_user = [user.coordinates for user in users]
    return jsonify({'neighbors': neighbors_of_current_user})
