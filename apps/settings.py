"""
settings.py

Configuration for Flask app

"""


class Config(object):
    # Set secret key to use session
    SECRET_KEY = "policyinformer"
    debug = False


class Production(Config):
    debug = True
    CSRF_ENABLED = False
    ADMIN = "essemfly@gmail.com"
    SQLALCHEMY_DATABASE_URI = 'mysql+gaerdbms:///Liketalk?instance=policyinformer:essemfly0803'
    migration_directory = 'migrations'
