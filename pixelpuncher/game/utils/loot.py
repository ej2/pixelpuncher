import random

from pixelpuncher.game.utils.message import add_game_message
from pixelpuncher.game.utils.messages import item_dropped, no_loot, pixels_dropped_message
from pixelpuncher.item.utils import get_random_drop, add_item_type_to_player
from pixelpuncher.player.utils.collections import check_collections


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

                check_collections(player, item_type_dropped)

    if items_received == 0:
        add_game_message(player, no_loot(enemy))


def generate_pixels(player, enemy):
    if enemy.enemy_type.maximum_pixels > 0:
        pixels = random.randint(enemy.enemy_type.minimum_pixels, enemy.enemy_type.maximum_pixels)

        if pixels > 0:
            player.pixels += pixels
            player.save()

            add_game_message(player, pixels_dropped_message(pixels))
