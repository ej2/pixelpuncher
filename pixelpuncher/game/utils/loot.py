import random

from pixelpuncher.game.utils.message import add_game_message
from pixelpuncher.game.utils.messages import item_dropped, no_loot
from pixelpuncher.item.utils import get_random_drop, add_item_type_to_player


def generate_loot(player, enemy):
    items_received = 0

    if enemy.enemy_type.drop_table:
        drop_table = enemy.enemy_type.drop_table
        items_dropped = random.randint(1, drop_table.max_drops)

        for x in range(1, items_dropped):
            item_type_dropped = get_random_drop(drop_table)

            if item_type_dropped:
                items_received += 1
                item = add_item_type_to_player(item_type_dropped, player)
                add_game_message(player, item_dropped(item))

    if items_received == 0:
        add_game_message(player, no_loot(enemy))
