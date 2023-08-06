from uuid import uuid4

from flask import Flask
from flask_login import (
    current_user,
    login_user,
    LoginManager as FlaskLoginManager,
    UserMixin,
)


class LoginManager(FlaskLoginManager):
    def init_app(self, app: Flask) -> None:
        super().init_app(app)

        @self.user_loader
        def load_user(user_id: str) -> User:
            return User(user_id)

        @app.before_request
        def loging_user() -> None:
            if current_user.is_authenticated:
                return

            user_id = str(uuid4())
            user = User(user_id)
            login_user(user, remember=True)


class User(UserMixin):
    def __init__(self, user_id: str) -> None:
        self.id = user_id
