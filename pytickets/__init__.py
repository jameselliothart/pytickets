import os
from flask import Flask
from werkzeug.utils import import_string


def create_app(settings_object='pytickets.config.ProdConfig'):
    app = Flask(__name__)
    cfg = import_string(os.getenv('PYTICKETS_SETTINGS', settings_object))()
    app.config.from_object(cfg)

    @app.route('/hello')
    def hello():
        app_env = app.config.get('ENVIRONMENT')
        return f'ENVIRONMENT: {app_env}'

    return app
