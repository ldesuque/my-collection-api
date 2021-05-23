from bson.json_util import dumps
from flask import request
from utils.login_required import login_required

from documents.users import UsersCollection
from documents.collections import CollectionsCollection
from documents.sessions import SessionsCollection
from documents.invitations import InvitationsCollection

from . import collections


@collections.route('/collections', methods=['POST'])
@login_required
def new_collection():
    try:
        request_data = request.get_json()
        collection_id = CollectionsCollection().add(request_data, request.user)

        response = {"object": {"id": collection_id}, "errors": []}
        status_code = 201
    except Exception as error:
        response = {"object": {}, "errors": [str(error)]}
        status_code = 500

    return dumps(response), status_code

@collections.route('/collections/<collection_id>', methods=['GET'])
@login_required
def get_collection(collection_id):
    try:
        request_user = request.user
        user_id = request_user['id']
        collection = CollectionsCollection().get_collection_by_id(int(collection_id),
                                                                  user_id, invited_allowed=True)        
        response = {"object": collection, "errors": []}
        status_code = 200
            
    except Exception as error:
        response = {"object": {}, "errors": [str(error)]}
        status_code = 500

    return dumps(response), status_code

@collections.route('collections/edit/<collection_id>', methods=['POST'])
@login_required
def edit_collection(collection_id):
    try:
        request_data = request.get_json()
        user_id = request.user['id']
        CollectionsCollection().edit(int(collection_id), user_id, request_data)
        response = {"object": {}, "errors": []}
        status_code = 200
        
    except Exception as error:
        response = {"object": {}, "errors": [str(error)]}
        status_code = 500

    return dumps(response), status_code

@collections.route('collections/<collection_id>', methods=['DELETE'])
@login_required
def detele_collection(collection_id):
    try:
        user_id = request.user['id']
        CollectionsCollection().delete(int(collection_id), user_id)
        
        response = {"object": {}, "errors": []}
        status_code = 200
        
    except Exception as error:
        response = {"object": {}, "errors": [str(error)]}
        status_code = 500

    return dumps(response), status_code

@collections.route('collections/custom/<collection_id>', methods=['POST'])
@login_required
def add_image_to_collection(collection_id):
    try:
        request_data = request.get_json()
        user_id = request.user['id']
        CollectionsCollection().add_image(int(collection_id), user_id, request_data)
        
        response = {"object": {}, "errors": []}
        status_code = 200
        
    except Exception as error:
        response = {"object": {}, "errors": [str(error)]}
        status_code = 500

    return dumps(response), status_code

@collections.route('collections/custom/<collection_id>', methods=['DELETE'])
@login_required
def delete_image_from_collection(collection_id):
    try:
        request_data = request.get_json()
        user_id = request.user['id']
        CollectionsCollection().delete_image(int(collection_id), user_id, request_data)
        
        response = {"object": {}, "errors": []}
        status_code = 200
        
    except Exception as error:
        response = {"object": {}, "errors": [str(error)]}
        status_code = 500

    return dumps(response), status_code