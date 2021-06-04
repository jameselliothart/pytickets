import os
from flask import Flask


def create_app(settings_object='pytickets.config.DevConfig'):
    app = Flask(__name__)
    app.config.from_object(os.getenv('PYTICKETS_SETTINGS', settings_object))

    @app.route('/hello')
    def hello():
        x = app.config.get('ENVIRONMENT')
        return f'ENVIRONMENT: {x}'

    return app
