from flaskr import db


class Cxn(db.Model):
    """ Represents a TODO.
    TODO: Defining |Cxn| in a separate file causes a circular dependency."""
    __tablename__ = 'cxn'
    id = db.Column(db.Integer, primary_key=True)
    # The IP of the server the user has a websocket connection to.
    websocket_server = db.Column(db.String, nullable=False)
    # Note this will use the |tablename|.
    app_user_id = db.Column(
        db.Integer, db.ForeignKey('appuser.id'), nullable=False)
    # Note the relationship field will use the actual class name.
    app_user = db.relationship('AppUser', back_populates='cxn')


class AppUser(db.Model):
    """Represents a User."""
    __tablename__ = 'appuser'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    coordinates = db.Column(db.String)
    # Note the relationship field will use the actual class name.
    cxn = db.relationship('Cxn', back_populates='app_user')
