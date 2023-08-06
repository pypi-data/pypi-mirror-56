from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from werkzeug.local import LocalProxy

from escarpolette.player import Player


db = SQLAlchemy()
player = Player()


def init_app(app: Flask):
    CORS(app)
    Migrate(app, db)
    db.init_app(app)
    player.init_app(app)
