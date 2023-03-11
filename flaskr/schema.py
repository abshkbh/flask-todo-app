from flaskr import db


class Todo(db.Model):
    """ Represents a TODO.
    TODO: Defining |Todos| in a separate file causes a circular dependency."""
    __tablename__ = 'todo'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)
    # Note this will use the |tablename|.
    app_user_id = db.Column(
        db.Integer, db.ForeignKey('appuser.id'), nullable=False)
    # Note the relationship field will use the actual class name.
    app_user = db.relationship('AppUser', back_populates='todos')

    def get_json_dict(self):
        """Implements a light weight serialization for a Todos object."""
        return {'user': self.app_user.username, 'content': self.content}


class AppUser(db.Model):
    """Represents a User."""
    __tablename__ = 'appuser'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    # Note the relationship field will use the actual class name.
    todos = db.relationship('Todo', back_populates='app_user')
