from jsonschema import validate, ValidationError
from database import mongo


class UsersCollection():
    def __init__(self):
        self._users = mongo.db['users']

    def add(self, json_data):
        self._add_id(json_data)
        self._validate(json_data)
        self._users.insert_one(json_data)

        return self.find_one({'email': json_data['email']})

    def find_one(self, filter):
        return self._users.find_one(filter)

    def count(self):
        return self._users.count_documents({})

    def exists_with(self, email):
        return self.find_one({'email': email}) is not None

    def _add_id(self, json_data):
        new_user_id = self.count() + 1
        json_data['id'] = new_user_id

    def _validate(self, json_data):
        validate(instance=json_data, schema=self._json_schema())

    def _json_schema(self):
        schema = {
            "type": "object",
            "properties": {
                "id": {"type": "integer", "minimum": 0},
                "email": {"type": "string", "format": "email"},
                "username": {"type": "string"},
                "password": {"type": "string"},
            },
            "required": ["id", "email", "username", "password"],
            "additionalProperties": False
        }

        return schema
