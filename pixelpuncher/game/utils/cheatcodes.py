from annoying.functions import get_object_or_None
from pixelpuncher.game.models import CheatCode
from pixelpuncher.game.utils.game import daily_reset


class CheatDailyReset(object):
    def cheat(self, player):
        daily_reset(player)
        return "Daily reset complete!"


class CheatFullHealth(object):
    def cheat(self, player):
        player.current_health = player.total_health
        player.save()
        return "Health restored!"


class CheatFullEnergy(object):
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

            return True

    return False


def do_cheat(player, cheatcode):
    cheat_class = globals()[cheatcode.cheat_class]()
    message = cheat_class.cheat(player)

    return message
