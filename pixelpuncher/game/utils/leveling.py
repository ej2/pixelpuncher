from pixelpuncher.game.utils import game_settings
from pixelpuncher.game.utils.message import add_game_message
from pixelpuncher.game.utils.messages import player_level_up_message
from pixelpuncher.game.utils.skills import add_skills, level_skill


def level_up(player):
    player.level += 1
    player.total_energy += game_settings.ENERGY_GAINED_PER_LEVEL
    player.total_health += game_settings.HEALTH_GAINED_PER_LEVEL
    player.attribute_points += game_settings.ATTRIBUTE_POINTS_PER_LEVEL
    player.current_energy = player.total_energy
    player.current_health = player.total_health
    player.save()

    for skill in player.skills.all():
        level_skill(skill)

    add_game_message(player, player_level_up_message())
    add_skills(player, player.level)


def can_level_up(player):
    next_level = xp_required_for_level(player.level)

    if player.xp > next_level:
        return True
    else:
        return False


def xp_required_for_level_old(level):
    if level == 0:
        return 0
    else:
        previous_amount = xp_required_for_level(level - 1)
        growth_amount = (game_settings.XP_BASE_AMOUNT * game_settings.XP_GROWTH_PER_LEVEL * (level - 1))
        amount = game_settings.XP_BASE_AMOUNT + growth_amount + previous_amount

        return amount


def xp_required_for_level(level):
    """
    Uses a basic arithmetic sequence (or a triangular pattern) to calculate the xp required for a level
    :param level:
    :return: XP amount for that level
    """
    return game_settings.XP_BASE_AMOUNT * (level * (level + 1)) / 2
