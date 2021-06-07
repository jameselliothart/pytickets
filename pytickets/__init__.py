import os
from string import Template
from flask import Flask, redirect, g
from flask.helpers import url_for
from werkzeug.utils import import_string
from .config import OKTA_SECRETS_FILE
from flask_oidc import OpenIDConnect

oidc = OpenIDConnect()


def create_app(settings_object='pytickets.config.ProdConfig'):
    app = Flask(__name__)
    cfg = import_string(os.getenv('PYTICKETS_SETTINGS', settings_object))()
    app.config.from_object(cfg)

    save_config(configure_okta, f'{OKTA_SECRETS_FILE.replace(".json",".template.json")}',
                f'{OKTA_SECRETS_FILE}')

    oidc.init_app(app)

    @app.before_request
    def before_request():
        g.environment = app.config.get('ENVIRONMENT')  # pylint: disable=assigning-non-slot
        if oidc.user_loggedin:
            g.user = oidc.user_getinfo(  # pylint: disable=assigning-non-slot
                ["sub", "name", "email"])
        else:
            g.user = None  # pylint: disable=assigning-non-slot

    from . import home
    app.register_blueprint(home.bp)
    app.add_url_rule('/', endpoint='home.index')

    from . import tickets
    app.register_blueprint(tickets.bp)

    return app


def configure_okta(
    template_content,
    client_id=os.getenv('OKTA_CLIENT_ID'),
    secret=os.getenv('OKTA_CLIENT_SECRET'),
    url=os.getenv('OKTA_ORG_URL'),
    uris=os.getenv('OKTA_REDIRECT_URIS')
):
    vars = {
        "OKTA_CLIENT_ID": client_id,
        "OKTA_CLIENT_SECRET": secret,
        "OKTA_ORG_URL": url,
        "OKTA_REDIRECT_URIS": uris,
    }
    return Template(template_content).substitute(**vars)


def save_config(configure, template_path, final_path):
    with open(template_path) as f:
        content = f.read()
    final = configure(content)
    with open(final_path, 'w') as f:
        print(final, file=f)
