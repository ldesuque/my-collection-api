import json
from functools import wraps
from flask import request

from documents.sessions import SessionsCollection
from documents.users import UsersCollection

def login_required(f, role=None):
    @wraps(f)
    def decorated_view(*args, **kwargs):
        token = request.headers.get('Authorization')
        session = SessionsCollection().find_one(token=token)
        if session is None:
            return json.dumps({"object": {}, "errors": [f"Invalid access token {token}"]}), 403

        request.user = UsersCollection().find_one({'email': session['email']})

        return f(*args, **kwargs)

    return decorated_view