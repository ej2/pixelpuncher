from pixelpuncher.game.utils.message import add_game_message
from pixelpuncher.item.utils import get_random_drop, add_item_type_to_player


def generate_loot(player, enemy):
    item_type_dropped = None

    if enemy.enemy_type.drop_table:
        item_type_dropped = get_random_drop(enemy.enemy_type.drop_table)

    if item_type_dropped:
        add_item_type_to_player(item_type_dropped, player)
        result = "You find a {0} on the {1}.".format(item_type_dropped.name, enemy)
    else:
        result = "You find nothing on the {0}.".format(enemy)

    add_game_message(player, result)
