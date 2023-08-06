from escarpolette.extensions import db
from datetime import datetime
from sqlalchemy import text


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(
        db.DateTime,
        default=datetime.now,
        server_default=text("datetime()"),
        index=True,
        nullable=False,
    )

    artist = db.Column(db.String(255))
    duration = db.Column(db.Integer)
    played = db.Column(db.Boolean, default=False, server_default=text("FALSE"))
    title = db.Column(db.String(255))
    url = db.Column(db.String(255), unique=True)
    user_id = db.Column(db.String(36), index=True, nullable=False)
