from bson.json_util import dumps
from flask import request

from documents.moodboards import MoodboardsCollection

from . import moodboards


@moodboards.route('/moodboards', methods=['GET'])
def get_moodborads():
    try:
        result = MoodboardsCollection().get_moodboards()

        response = {"object": result, "errors": []}
        status_code = 200
    except Exception as error:
        response = {"object": {}, "errors": [str(error)]}
        status_code = 500

    return dumps(response), status_code

@moodboards.route('/moodboards/trend', methods=['GET'])
def get_trend_by_id():
    try:
        request_data = request.get_json()
        trend_id = request_data['trend_id']
        
        trend = MoodboardsCollection().get_trend_by_id(trend_id)        
        response = {"object": trend, "errors": []}
        status_code = 200
            
    except Exception as error:
        response = {"object": {}, "errors": [str(error)]}
        status_code = 500

    return dumps(response), status_code