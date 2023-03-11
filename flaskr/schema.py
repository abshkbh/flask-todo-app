from flaskr import db


class Todos(db.Model):
    """ Represents a TODO.
    TODO: Defining |Todos| in a separate file causes a circular dependency."""
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', back_populates='todos')

    def get_json_dict(self):
        """Implements a light weight serialization for a Todos object."""
        return {'user': self.user.username, 'content': self.content}


class User(db.Model):
    """Represents a User."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    todos = db.relationship('Todos', back_populates='user')
