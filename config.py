import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    TESTING = False
    APP_NAME = 'tz_ubi'
    PAGE_TITLE = "LG's Timezone API"
    SECRET_KEY = 'Would be Great to Work for UBIMET'

class ProductionConfig(Config):
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True