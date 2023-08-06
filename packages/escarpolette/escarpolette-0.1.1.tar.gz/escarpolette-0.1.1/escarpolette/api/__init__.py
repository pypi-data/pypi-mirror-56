from flask_restplus import Api

from .items import ns as items_ns
from .player import ns as player_ns

api = Api(
    version="0.1",
    title="Escarpolette",
    description="Manage your party's playlist without friction",
)

api.add_namespace(items_ns)
api.add_namespace(player_ns)
