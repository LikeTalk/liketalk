"""
settings.py

Configuration for Flask app

"""


class Config(object):
    # Set secret key to use session
    SECRET_KEY = "planfindtheir"
    debug = False


class Production(Config):
    debug = True
    CSRF_ENABLED = False
    ADMIN = "khszone02@gmail.com"
    SQLALCHEMY_DATABASE_URI = 'mysql+gaerdbms:///comment?instance=planfindtheir:findtheir'
    migration_directory = 'migrations'
