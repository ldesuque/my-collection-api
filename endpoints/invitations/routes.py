from bson.json_util import dumps
from flask import request
from utils.login_required import login_required

from documents.invitations import InvitationsCollection

from . import invitations


@invitations.route('/invitations', methods=['POST'])
@login_required
def new_invitation():
    try:
        request_data = request.get_json()
        user_id = request.user['id']
        InvitationsCollection().add(request_data, user_id)

        response = {"object": {}, "errors": []}
        status_code = 201
    except Exception as error:
        response = {"object": {}, "errors": [str(error)]}
        status_code = 500

    return dumps(response), status_code
