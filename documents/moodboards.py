
from jsonschema import validate, ValidationError
from database import mongo


class MoodboardsCollection():
    def __init__(self):
        self._moodboards = mongo.db['moodboards']

    def get_moodboards(self):
        hide_info = {'_id': 0}
        
        return self._moodboards.find(projection=hide_info)
    
    def get_trend_by_id(self, trend_id):
        filter = {'id': trend_id}
        hide_info = {'_id': 0}
        
        trend = self._moodboards.find_one(filter, hide_info)
        self._validate_not_empty_trend(trend, trend_id)
        
        return trend
    
    def _validate_not_empty_trend(self, trend, trend_id):
        if not trend:
            raise ValidationError(
                f"Trend id: {trend_id} not found.")
