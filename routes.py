from endpoints.users.routes import users
from endpoints.collections.routes import collections
from endpoints.invitations.routes import invitations
from endpoints.moodboards.routes import moodboards


def register_endpoints(app):
    app.register_blueprint(users, url_prefix='/api/')
    app.register_blueprint(collections, url_prefix='/api/')
    app.register_blueprint(invitations, url_prefix='/api/')
    app.register_blueprint(moodboards, url_prefix='/api/')
