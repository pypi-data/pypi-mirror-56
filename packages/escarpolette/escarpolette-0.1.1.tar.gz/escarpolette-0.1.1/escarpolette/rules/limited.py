from dataclasses import dataclass

from sqlalchemy import func

from escarpolette.models.item import Item
from escarpolette.user import User


@dataclass
class RulesConfig:
    MAX_ITEM_NUMBER: int = 3
    MAX_ITEM_LENGTH: int = 600


class Rules:
    def __init__(self, config: RulesConfig) -> None:
        self.config = config

    def can_add_item(self, user: User, item: Item) -> bool:
        if item.duration > self.config.MAX_ITEM_LENGTH:
            return False

        count = Item.query.filter(
            Item.created_at >= func.now(), Item.user_id == user.id
        ).count()

        return count < self.config.MAX_ITEM_NUMBER

    def can_remove_item(self, user: User) -> bool:
        return False

    def can_toogle_pause(self, user: User) -> bool:
        return False

    def can_vote(self, user: User, item: Item) -> bool:
        return False
