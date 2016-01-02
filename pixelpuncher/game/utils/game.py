from pixelpuncher.game.utils.message import add_game_message
from pixelpuncher.game.utils.messages import out_of_health_message, out_of_punches_message


def can_punch(player):

    if player.current_health == 0:
        add_game_message(player, out_of_health_message())
        return False

    if player.punches <= 0:
        add_game_message(player, out_of_punches_message())
        return False

    return True
