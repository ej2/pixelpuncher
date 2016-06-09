import random

from annoying.functions import get_object_or_None

from pixelpuncher.enemy.models import Enemy
from pixelpuncher.game.utils.message import add_game_message
from pixelpuncher.game.utils.messages import battle_message
from pixelpuncher.player.models import COMBAT


def get_enemy(player, location):
    enemy = get_current_enemy(player)

    if enemy is None:
        enemy = random_encounter(player, location)
        player.status = COMBAT
        player.punches -= 1  # Should each attack cost one punch or each combat?
        player.save()

        add_game_message(player, battle_message(enemy))

    return enemy


def get_current_enemy(player):
    return get_object_or_None(Enemy, active=True, player=player)


def random_encounter(player, location):
    enemy_spawns = location.enemy_spawns.filter(enemy_type__base_level__lte=player.level)
    enemy_spawn = random.choice(enemy_spawns)

    enemy = create_enemy(enemy_spawn.enemy_type, player)
    return enemy


def create_enemy(enemy_type, player):
    enemy = Enemy()

    level_bonus = random.randint(0, 2)  # increases difficultly slightly
    enemy.level = enemy_type.base_level + level_bonus

    enemy.enemy_type = enemy_type
    enemy.player = player

    enemy.total_health = random.randint(enemy_type.minimum_health, enemy_type.maximum_health) + (level_bonus * 5)
    enemy.current_health = enemy.total_health

    enemy.attack = enemy_type.attack + (level_bonus * 2)
    enemy.defense = enemy_type.defense + (level_bonus * 2)

    enemy.number_of_dice = enemy_type.number_of_dice
    enemy.dice_sides = enemy_type.dice_sides
    enemy.bonus = enemy_type.bonus + level_bonus

    enemy.save()

    return enemy
