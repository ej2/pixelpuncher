import datetime
from django.utils import timezone

from pixelpuncher.game.utils import game_settings
from pixelpuncher.game.utils.message import add_game_message
from pixelpuncher.game.utils.messages import out_of_health_message, out_of_punches_message


def can_punch(player):
    if player.current_health == 0:
        death(player)
        return False

    if player.punches <= 0:
        add_game_message(player, out_of_punches_message())
        return False

    return True


def reset_check(player):
    if player.date_last_punch_reset < timezone.now() - datetime.timedelta(hours=game_settings.RESET_FREQUENCY):
        return True

    return False


def daily_reset(player):
    player.punches = game_settings.DAILY_PUNCHES
    player.date_last_punch_reset = timezone.now()
    player.save()


def death(player):
    add_game_message(player, out_of_health_message())

    # handle death pently


