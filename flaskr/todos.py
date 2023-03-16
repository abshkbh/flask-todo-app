from flaskr.schema import Todo
from flaskr import db
from flask import Blueprint, jsonify, request, abort
from flask_jwt_extended import jwt_required, get_jwt_identity

bp = Blueprint('todos', __name__, url_prefix='/todos')


@bp.route('/add', methods=['POST'])
@jwt_required()
def add():
    """Add a new todo."""

    request_json = request.get_json()
    if not request_json:
        abort(400, {'error': 'no JSON data in the request'})

    content = request_json.get('content')
    if not content:
        abort(400, {'error': 'no content'})

    current_user_id = get_jwt_identity()
    todo = Todo(content=content, app_user_id=current_user_id)
    db.session.add(todo)
    db.session.commit()
    return jsonify()


@bp.route('/list', methods=['GET'])
@jwt_required()
def todos_list():
    """Returns all todos for the registered user."""

    current_user_id = get_jwt_identity()
    todos = Todo.query.filter_by(app_user_id=current_user_id).all()
    # This returns a list of dicts.
    todos_json = [todo.get_json_dict() for todo in todos]
    return jsonify({'todos': todos_json})
