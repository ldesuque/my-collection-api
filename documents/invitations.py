from jsonschema import validate, ValidationError
from database import mongo


class InvitationsCollection():
    def __init__(self):
        self._invitations = mongo.db['invitations']

    def add(self, json_data, user_id):
        self._validate(json_data)
        self._validate_unique(json_data)
        self._validate_collection_id(json_data, user_id)
        self._invitations.insert_one(json_data)
    
    def user_has_access(self, invited_id, collection_id):
        filter = {"collection_id": collection_id}
        hide_info = { '_id': 0 }
        
        invitations = list(self._invitations.find(filter, hide_info))
        
        for invitation in invitations:
            if invitation['invited_id'] == invited_id:
                return True
        
        return False
    
    def _find_by(self, filter, hide_info):
        return list(self._invitations.find(filter, hide_info))
    
    def _validate_unique(self, json_data):
        if self._invitations.find_one({'collection_id': json_data['collection_id'],
                                       'invited_id': json_data['invited_id']}) is not None:
            raise ValidationError(f"The user already has read permissions on this collection")
    
    def _validate_collection_id(self, json_data, owner_id):
        invited_id = json_data['invited_id']
        
        if owner_id == invited_id:
            raise ValidationError(f"The owner cannot be invited to his own collection")
    
    def _validate(self, json_data):
        validate(instance=json_data, schema=self._json_schema())

    def _json_schema(self):
        schema = {
            "type": "object",
            "properties": {
                "collection_id": {"type": "integer", "minimum": 0},
                "invited_id": {"type": "integer", "minimum": 0},
            },
            "required": ["collection_id", "invited_id"],
            "additionalProperties": False
        }
        return schema