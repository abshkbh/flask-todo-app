from flaskr.schema import Todos
from flaskr.auth import login_required
from flaskr import db
from flask import Blueprint, jsonify, request, abort, g

bp = Blueprint('todos', __name__, url_prefix='/todos')


@bp.route('/add', methods=['POST'])
@login_required
def add():
    """Add a new todo."""
    request_json = request.get_json()
    if not request_json:
        abort(400, {'error': 'no JSON data in the request'})

    content = request_json.get('content')
    if not content:
        abort(400, {'error': 'no content'})

    todo = Todos(content=content, user_id=g.user.id)
    db.session.add(todo)
    db.session.commit()
    return jsonify()


@bp.route('/list', methods=['GET'])
@login_required
def list():
    """Returns all todos for the registered user."""
    todos = Todos.query.filter_by(user_id=g.user.id).all()
    todos_json = [todo.get_json_dict() for todo in todos]
    return jsonify({'todos': todos_json})
