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

    def login(self, json_data):
        filter = {'email': json_data['email']}
        user = self.find_one(filter)
        
        self._validate_password(user, json_data['password'])
        return user
    
    def find_one(self, filter):       
        return self._users.find_one(filter)

    def count(self):
        return self._users.count_documents({})

    def exists_with(self, email):
        user = self._users.find_one({'email': email})
        return user is not None

    # Why did I include this method (_validate_password)? Because the main idea of this API
    # is not the security, so I programmed the basic idea behind a token security method.
    #
    #  Things we should refactor:
    # * This method is beyond the responsibilities of the class, and should be included in another
    # * class to respect SOLID principles.
    #
    # * The passwords are stored in plain text in the database, and they are sent in the body of
    # * our request. This implementation is susceptible to men in the middle attacks. We could solve 
    # * it sending the request through a https connection.
    def _validate_password(self, user, entered_password):
        if user['password'] != entered_password:
            raise ValidationError(f"Invalid password.")

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
                "password": {"type": "string"},
            },
            "required": ["id", "email", "password"],
            "additionalProperties": False
        }

        return schema
