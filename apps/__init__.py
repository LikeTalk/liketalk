"""
Initialize Flask app

"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = Flask('apps')
app.config.from_object('apps.settings.Production')

db = SQLAlchemy(app)
manager = Manager(app)
migrate = Migrate(app,db)
manager.add_command('db',MigrateCommand)

#import models, admin, candidate, comment, debug, test, tournament, user_account, view_page, what_match
import models, view_page
#(Guess - Export)

