import random

from pixelpuncher.game.models import GameMessage


ATTACK_VERBS = ("swings", "claws", "scratches", "hits", "kicks",)
PAIN_WORDS = ("Ouch!", "Yozzers!", "Argh!", "Gah!", "Oww!", "Yeow!", "Yikes!")
PUNCH_SOUNDS = ("BAM!", "CRASH!", "ZAP!", "KAPOW!", "POP!")
DESTROYED_VERBS = ("shattered", "flattened", "crushed", "smashed", "splattered")
TAUNTS = (
    "Your mother was a hamster and your father smelt of elderberries!",
    "Have a knuckle sandwich!",
)


def add_game_message(player, message):
    game_message = GameMessage()
    game_message.player = player
    game_message.message = message
    game_message.save()


def get_game_messages(player):
    messages = GameMessage.objects.filter(player=player, shown=False).order_by("date_created")

    for message in messages:
        message.shown = True
        message.save()

    return messages


def get_random_attack_verbs():
    return random.choice(ATTACK_VERBS)


def get_random_pain_word():
    return random.choice(PAIN_WORDS)


def get_random_punching_sound():
    return random.choice(PUNCH_SOUNDS)


def get_random_destroyed_word():
    return random.choice(DESTROYED_VERBS)


class GameMessageManager(object):
    _message = ""

    def add(self, message, pause=50):
        self._message += "{}^{}\\n".format(message, pause)

    def to_string(self):
        return self._message
