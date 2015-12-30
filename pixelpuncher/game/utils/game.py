from pixelpuncher.game.utils.message import add_game_message


def can_punch(player):

    if player.current_health == 0:
        add_game_message(player, "Your hands hurt too much right now to punch stuff.")
        return False

    if player.punches <= 0:
        add_game_message(player, "You are tired of punching stuff right now.")
        return False

    return True
