from jsonschema import validate, ValidationError
from database import mongo


class MoodboardsCollection():
    def __init__(self):
        self._moodboards = mongo.db['moodboards']

    def _validate(self, json_data):
        validate(instance=json_data, schema=self._json_schema())

    def _json_schema(self):
        schema = {
            "type": "object",
            "properties": {
                "comments": {"type": "integer"},
                "likes": {"type": "integer"},
                "panel_name": {"type": "array",
                               "items": [{"type": "string"}]
                               },
            },
            "required": ["id", "user_id", "name"],
            "additionalProperties": False
        }

        return schema
