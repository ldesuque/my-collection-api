from flask import Flask
from settings import Config
from database import mongo

from routes import register_endpoints


def create_app():
    app = Flask(__name__)
    environment_config = Config.for_actual_environment()

    app.config.from_object(environment_config)
    mongo.init_app(app)
    register_endpoints(app)

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0')
