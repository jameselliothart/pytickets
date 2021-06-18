import os

_DUMMY_SECRET = 'a-dummy-key'
OKTA_SECRETS_FILE = 'pytickets/client_secrets.json'


def _check_secret(secret, dummy_secret):
    if secret == dummy_secret or len(secret) == 0:
        raise ValueError('Must set PYTICKETS_SECRET_KEY')
    return True


class Config():
    ENVIRONMENT = 'BASE'
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv('PYTICKETS_SECRET_KEY', _DUMMY_SECRET)

    OIDC_CLIENT_SECRETS = OKTA_SECRETS_FILE
    OIDC_ID_TOKEN_COOKIE_SECURE = os.getenv(
        'OKTA_REDIRECT_URIS')[:5] == 'https'
    OIDC_CALLBACK_ROUTE = "/oidc/callback"
    OIDC_SCOPES = ["openid", "email", "profile"]


class TestConfig(Config):
    ENVIRONMENT = 'TEST'
    TESTING = True


class DevConfig(Config):
    ENVIRONMENT = 'DEV'
    DEBUG = True


class ProdConfig(Config):
    ENVIRONMENT = 'PROD'

    def __init__(self):
        self._check = _check_secret(self.SECRET_KEY, _DUMMY_SECRET)


def get_datebase_uri():
    uri = os.environ['DATABASE_URL']
    uri = uri.replace("postgres://", "postgresql://", 1)
    return uri
