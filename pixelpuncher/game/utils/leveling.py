from pixelpuncher.game.utils import game_settings
from pixelpuncher.game.utils.message import add_game_message


def level_up(player):
    player.level += 1
    player.total_energy += game_settings.ENERGY_GAINED_PER_LEVEL
    player.total_health += game_settings.HEALTH_GAINED_PER_LEVEL
    player.current_energy = player.total_energy
    player.current_health = player.total_health
    player.save()

    add_game_message(player, "<span class='level-up'>LEVEL UP!</span>")


def can_level_up(player):
    next_level = xp_required_for_level(player.level + 1)

    if player.xp > next_level:
        return True
    else:
        return False


def xp_required_for_level(level):
    if level == 0:
        return 0
    else:
        previous_amount = xp_required_for_level(level - 1)
        growth_amount = (game_settings.XP_BASE_AMOUNT * game_settings.XP_GROWTH_PER_LEVEL * (level - 1))
        amount = game_settings.XP_BASE_AMOUNT + growth_amount + previous_amount

        return amount
