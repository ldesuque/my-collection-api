from endpoints.users.routes import users
from endpoints.collections.routes import collections
from endpoints.invitations.routes import invitations


def register_endpoints(app):
    app.register_blueprint(users, url_prefix='/api/')
    app.register_blueprint(collections, url_prefix='/api/')
    app.register_blueprint(invitations, url_prefix='/api/')
    