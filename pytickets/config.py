import os

_DUMMY_SECRET = 'a-dummy-key'


def _check_secret(secret, dummy_secret):
    if secret == dummy_secret or secret is None or len(secret) == 0:
        raise ValueError('Must set PYTICKETS_SECRET_KEY')
    return True


class Config():
    ENVIRONMENT = 'BASE'
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv('PYTICKETS_SECRET_KEY', _DUMMY_SECRET)


class TestConfig(Config):
    ENVIRONMENT = 'TEST'
    TESTING = True


class DevConfig(Config):
    ENVIRONMENT = 'DEV'
    DEBUG = True


class ProdConfig(Config):
    ENVIRONMENT = 'PROD'
    _CHECK = _check_secret(os.getenv('PYTICKETS_SECRET_KEY'), _DUMMY_SECRET)
