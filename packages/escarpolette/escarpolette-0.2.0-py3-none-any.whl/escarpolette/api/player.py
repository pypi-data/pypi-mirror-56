from typing import Dict

from flask import request
from flask_restplus import Namespace, Resource, fields
from werkzeug.exceptions import BadRequest

from escarpolette.extensions import player
from escarpolette.player import State

ns = Namespace("player", description="Manage the player state")

player_model = ns.model(
    "Player", {"state": fields.String(enum=[x.name for x in State], required=True)}
)


@ns.route("/")
class Player(Resource):
    @ns.marshal_list_with(player_model)
    def get(self) -> Dict:
        data = {"state": player.get_state().name}
        return data

    @ns.expect(player_model)
    @ns.response(200, "Player state changed")
    @ns.response(400, "Invalid state")
    def patch(self) -> None:
        data = request.get_json()
        if data["state"] == State.PLAYING:
            player.play()
        elif data["state"] == State.PAUSED:
            player.pause()
        else:
            raise BadRequest(f"The state f{data['state']} cannot be set.")
