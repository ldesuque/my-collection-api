from jsonschema import validate, ValidationError

from database import mongo
from utils.random_string import random_string


class SessionsCollection:
    TOKEN_LENGTH = 20
    LOGIN_FAILED_ERROR_MESSAGE = "The data is not valid"

    def __init__(self):
        self._sessions = mongo.db['sessions']

    def create_for(self, user):
        data = {
            "email": user['email'],
        }
        token = random_string(self.TOKEN_LENGTH)
        data['token'] = token

        self._validate(data)
        self._sessions.insert_one(data)
        return token

    def remove_for(self, user):
        session = self.find_by_email(user['email'])
        if session is None:
            raise ValidationError(f"The session token is not valid")

        self._sessions.delete_one({"token": session['token']})

    def find_one(self, token):
        return self._sessions.find_one({"token": token})

    def find_by_email(self, email):
        return self._sessions.find_one({"email": email})

    def _validate(self, json_data):
        validate(instance=json_data, schema=self._json_schema())

    def _json_schema(self):
        schema = {
            "type": "object",
            "properties": {
                "email": {"type": "string", "format": "email"},
                "token": {
                    "type": "string",
                    "minLength": SessionsCollection.TOKEN_LENGTH,
                    "maxLength": SessionsCollection.TOKEN_LENGTH
                },
            },
            "required": ["email", "token"],
            "additionalProperties": False
        }
        
        return schema