import random

from annoying.functions import get_object_or_None

from pixelpuncher.enemy.models import Enemy, EnemyType
from pixelpuncher.game.utils.message import add_game_message
from pixelpuncher.player.models import COMBAT


def get_enemy(player):
    enemy = get_current_enemy(player)

    if enemy is None:
        enemy = random_encounter(player)
        player.status = COMBAT
        player.save()

        add_game_message(player, "You see a {0}.".format(enemy))
    else:
        add_game_message(player, "You are battling a {0}.".format(enemy))

    return enemy


def get_current_enemy(player):
    return get_object_or_None(Enemy, active=True, player=player)


def random_encounter(player):
    enemy_types = EnemyType.objects.filter(base_level__lte=player.level)
    enemy_type = random.choice(enemy_types)

    enemy = create_enemy(enemy_type, player)
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
