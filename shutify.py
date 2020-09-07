import os
import click
from flask_migrate import Migrate
from app import create_app
from app.extensions import db

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)
