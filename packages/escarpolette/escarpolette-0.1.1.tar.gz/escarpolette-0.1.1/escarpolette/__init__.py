from flask import Flask

from escarpolette.api import api
from escarpolette.user import LoginManager
from escarpolette.settings import Default as DefaultSettings
from escarpolette import extensions

app = Flask(__name__, instance_relative_config=True)
app.config.from_object(DefaultSettings(app))
app.config.from_pyfile("application.cfg", silent=True)

api.init_app(app)
extensions.init_app(app)
LoginManager().init_app(app)
