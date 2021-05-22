from jsonschema import validate, ValidationError
from database import mongo

from documents.invitations import InvitationsCollection


class CollectionsCollection():
    def __init__(self):
        self._collections = mongo.db['collections']

    def add(self, json_data, user):
        self._add_id(json_data)
        self._add_user_id(json_data, user)
        self._add_deleted_info(json_data)
        self._validate(json_data)
        self._collections.insert_one(json_data)

        new_collection_id = json_data['id']
        return new_collection_id

    def edit(self, collection_id, user_id, json_data):
        collection = self.get_collection_by_id(collection_id, user_id, invited_allowed=False)
        self._collections.update_one({'id': collection['id']}, {
                                     "$set": {'name': json_data['name']}})

    def delete(self, collection_id, user_id):
        collection = self.get_collection_by_id(collection_id, user_id, invited_allowed=False)
        self._collections.update_one({'id': collection['id']}, {
                                     "$set": {'deleted': True}})

    def get_collections_created_by(self, user_id):
        filter = {'user_id': user_id,
                  'deleted': False}
        hide_info = {'_id': 0,
                     'user_id': 0,
                     'deleted': 0}

        return list(self._collections.find(filter, hide_info))

    def get_collection_by_id(self, collection_id, user_id, invited_allowed=False):
        filter = {'id': collection_id,
                  'deleted': False}
        hide_info = {'_id': 0,
                     'deleted': 0}

        collection = self._collections.find_one(filter, hide_info)

        self._validate_not_empty_collection(collection, collection_id)

        if not invited_allowed:
            self._validate_ownership(user_id, collection)
        elif not self._is_owner_of_collection(user_id, collection):
            self._validate_invitation(user_id, collection_id)
        
        return collection

    def count(self):
        return self._collections.count_documents({})

    def _validate_not_empty_collection(self, collection, collection_id):
        if not collection:
            raise ValidationError(
                f"Collection id: {collection_id} not found.")

    def _validate_ownership(self, user_id, collection):
        if not self._is_owner_of_collection(user_id, collection):
            raise ValidationError(
                f"Collection id: {collection['id']} is private.")

    def _validate_invitation(self, user_id, collection_id):
        if not InvitationsCollection().user_has_access(user_id, collection_id):
            raise ValidationError(
                f"Collection id: {collection_id} is private.")
    
    def _is_owner_of_collection(self, user_id, collection):
        return collection['user_id'] == user_id

    def _add_id(self, json_data):
        new_collection_id = self.count() + 1
        json_data['id'] = new_collection_id

    def _add_deleted_info(self, json_data):
        json_data['deleted'] = False

    def _add_user_id(self, json_data, user):
        json_data['user_id'] = user['id']

    def _validate(self, json_data):
        validate(instance=json_data, schema=self._json_schema())

    # TODO It would be nice to add: creation_date, updated_at, description
    def _json_schema(self):
        schema = {
            "type": "object",
            "properties": {
                "id": {"type": "integer", "minimum": 0},
                "user_id": {"type": "integer"},
                "name": {"type": "string"},
                "deleted": {"type": "boolean"}
            },
            "required": ["id", "user_id", "name"],
            "additionalProperties": False
        }

        return schema
