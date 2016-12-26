from annoying.functions import get_object_or_None
from pixelpuncher.game.models import CheatCode
from pixelpuncher.game.utils.game import daily_reset
from pixelpuncher.game.utils.message import add_game_message


class CheatBase(object):
    def unlock(self, player):
        raise NotImplementedError

    def cheat(self, player):
        raise NotImplementedError


class CheatNothing(CheatBase):
    def unlock(self, player):
        return "My eyes! The cheat does nothing!"

    def cheat(self, player):
        return "My eyes! The cheat does nothing!"


class Cheat1000Pixels(CheatBase):
    def unlock(self, player):
        player.pixels += 1000
        player.save()
        return "Woohoo! You receive 1000 pixels."

    def cheat(self, player):
        return "You already got your handout..."


class CheatDailyReset(CheatBase):
    def unlock(self, player):
        return "Daily reset unlocked!"

    def cheat(self, player):
        daily_reset(player)
        return "Daily reset complete!"


class CheatFullHealth(CheatBase):
    def unlock(self, player):
        return "Full health cheat unlocked!"

    def cheat(self, player):
        player.current_health = player.total_health
        player.save()
        return "Health restored!"


class CheatAPGain(CheatBase):
    def unlock(self, player):
        return "Gain AP cheat unlocked!"

    def cheat(self, player):
        player.attribute_points += 1
        player.save()
        return "You gained an attribute point!"


class CheatFullEnergy(CheatBase):
    def unlock(self, player):
        return "Full energy cheat unlocked!"

    def cheat(self, player):
        player.current_energy = player.total_energy
        player.save()
        return "Energy restored!"


def add_cheatcode(player, code):
    cheat_code = get_object_or_None(CheatCode, code=code, admin_only=False)

    if cheat_code:
        if player not in cheat_code.players.all():
            cheat_code.players.add(player)
            cheat_code.save()

            cheat_class = get_cheat_class(cheat_code)
            result = cheat_class.unlock(player)
            add_game_message(player, result)

            return True

    return False


def get_cheat_class(cheatcode):
    return globals()[cheatcode.cheat_class]()


def do_cheat(player, cheatcode):
    cheat_class = get_cheat_class(cheatcode)
    message = cheat_class.cheat(player)

    return message
