import ndjson

from flask import Flask
from settings import Config
from database import mongo

from routes import register_endpoints
from documents.moodboards import MoodboardsCollection

ndjson_file = "./data/sample_moodboard.ndjson"


# Only for testing in development and test environments
def _initialize_data():
    try:
        with open(ndjson_file) as f:
            data = ndjson.load(f)
        
        mongo.db['moodboards'].insert_many(data)
    except Exception as error:
        print('Data initializer error: ' + str(error))

def create_app():
    app = Flask(__name__)
    environment_config = Config.for_actual_environment()

    app.config.from_object(environment_config)
    mongo.init_app(app)
    register_endpoints(app)

    # I am assuming that the data from the initialization file is available 
    # (either via elasticsearch or another database), so in a test or development 
    # environment, I load the data manually.
    # We should make a refactor to bring this functionality to the production environment
    if environment_config.need_initialization():
        _initialize_data()

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0')
