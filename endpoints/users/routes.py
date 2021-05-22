from bson.json_util import dumps
from flask import request
from utils.login_required import login_required

from documents.users import UsersCollection
from documents.collections import CollectionsCollection
from documents.sessions import SessionsCollection
from . import users


#TODO Login compare password
@users.route('/users/add-and-login', methods=['POST'])
def add_user():
    try:
        request_data = request.get_json()
        users_collection = UsersCollection()

        if users_collection.exists_with(email=request_data['email']):
            new_user_created = False
            user = users_collection.find_one({'email': request_data['email']})
        else:
            new_user_created = True
            user = users_collection.add(json_data=request_data)
        
        token = SessionsCollection().create_for(user)
        response = {"object": {
                "new_user_created": new_user_created, "token": token, "user": user, "errors": []}}
        status_code = 200
    except Exception as error:
        response = {"object": {}, "errors": [str(error)]}
        status_code = 500

    return dumps(response), status_code

@users.route('/users/logout', methods=['POST'])
@login_required
def logout_user():
    try:
        SessionsCollection().remove_for(request.user)
        response = {"object": {}, "errors": []}
        status_code = 200
    except Exception as error:
        response = {"object": {}, "errors": [str(error)]}
        status_code = 500
        
    return dumps(response), status_code

@users.route('/users/collections', methods=['GET'])
@login_required
def get_user_collections():
    try:
        result = CollectionsCollection().get_collections_created_by(request.user['id'])
        response = {"object": result, "errors": []}
        status_code = 200
    except Exception as error:
        response = {"object": {}, "errors": [str(error)]}
        status_code = 500
        
    return dumps(response), status_code


