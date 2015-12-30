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
    enemy_types = EnemyType.objects.all()
    enemy_type = random.choice(enemy_types)

    enemy = create_enemy(enemy_type, player)
    return enemy


def create_enemy(enemy_type, player):
    enemy = Enemy()

    enemy.player = player
    enemy.enemy_type = enemy_type
    enemy.hits = 0
    enemy.level = enemy_type.base_level + random.randint(0, 2)

    enemy.total_health = random.randint(enemy_type.minimum_health, enemy_type.maximum_health)
    enemy.current_health = enemy.total_health
    enemy.damage = enemy_type.base_damage
    enemy.save()

    return enemy
