from typing import Dict

from flask import request
from flask_login import current_user, login_required
from flask_restplus import Namespace, Resource, fields
from werkzeug.exceptions import BadRequest, TooManyRequests

from escarpolette.extensions import db, player
from escarpolette.models import Item
from escarpolette.tools import get_content_metadata
from escarpolette.rules import rules

ns = Namespace("items", description="Manage the playlist's items")

item = ns.model(
    "Item",
    {
        "artist": fields.String(readonly=True),
        "duration": fields.Integer(readonly=True),
        "title": fields.String(readonly=True),
        "url": fields.Url(
            absolute=True,
            example="https://www.youtube.com/watch?v=bpA6fAz_r04",
            required=True,
        ),
    },
)

playlist = ns.model(
    "Playlist", {"idx": fields.Integer, "items": fields.List(fields.Nested(item))}
)


@ns.route("/")
class Items(Resource):
    @ns.marshal_list_with(playlist)
    @login_required
    def get(self) -> Dict:
        playlist = []
        playing_idx = 0

        for item in Item.query.order_by(Item.created_at).all():
            playlist.append(
                {
                    "artist": item.artist,
                    "duration": item.duration,
                    "title": item.title,
                    "url": item.url,
                }
            )
            if item.played:
                playing_idx += 1

        data = {"items": playlist, "idx": playing_idx}
        return data

    @ns.expect(item)
    @ns.marshal_with(item, code=201)
    @login_required
    def post(self) -> Dict:
        data = request.json

        if data is None:
            raise BadRequest("Missing data")

        metadata = get_content_metadata(data["url"])
        item = Item(user_id=current_user.id, **metadata)

        if not rules.can_add_item(current_user, item):
            raise TooManyRequests

        db.session.add(item)
        db.session.flush()

        player.add_item(item.url)

        db.session.commit()

        return metadata
