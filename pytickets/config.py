import os

class Config():
    ENVIRONMENT = 'BASE'
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv('PYTICKETS_SECRET_KEY', 'a-dummy-key')


class TestConfig(Config):
    ENVIRONMENT = 'TEST'
    TESTING = True


class DevConfig(Config):
    ENVIRONMENT = 'DEV'
    DEBUG = True


class ProdConfig(Config):
    ENVIRONMENT = 'PROD'