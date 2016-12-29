import random

from pixelpuncher.game.models import GameMessage


ATTACK_VERBS = ("swings", "claws", "scratches", "hits", "kicks",)
PAIN_WORDS = ("Ouch!", "Yozzers!", "Argh!", "Gah!", "Oww!", "Yeow!", "Yikes!")
PUNCH_SOUNDS = ("BAM!", "CRASH!", "ZAP!", "KAPOW!", "POP!")
DESTROYED_VERBS = ("shattered", "flattened", "crushed", "smashed", "splattered")

TAUNTS = (
    "Your mother was a hamster and your father smelt of elderberries!",
    "Have a knuckle sandwich!",
    "I fart in your general direction!",
    "Is that all you got?",
)

VICTORY_QUOTES = (
    "My fists know no equal!",
    "You can't defeat me with moves like that!",
    "You didn't keep your mind on the fight. That's why you lost!",
    "Size and strength are no use if you can't hit me.",
    "You were out of breath towards the end. You need to work on your stamina.",
    "Sorry to be blunt, but you just don't have what it takes to beat me.",
    "I don't need a reason. I just like to fight.",
    "Try not to get knocked out so quick next time, OK?",
    "Punching is the most refined of the fighting arts.",
    "Victory is mine!",
    "Your weakness is an embarrassment!",
    "That was too easy!",
    "I'm so tired... I can hardly wait to relax with a nice bubble bath.",
    "Each time I punch, I learn something new. This journey has been fruitful.",
    "You are not a warrior, you're a beginner.",
    "Awesome fight! I'm on top of my game today!",
    "No one compares to my beauty. Nor my strength.",
    "You did quite well, but you need more training to defeat me!",
    "To live is to punch, to punch is to live!"
)

DEFEAT_MESSAGES = (
    "Your hands hurt too much right now to punch stuff. Maybe you should have a refreshing sports drink.",
    "Your hands hurt too much right now to punch stuff. Maybe you should take a nap.",
    "Your hands hurt too much right now to punch stuff. Maybe you should train more.",
    "You are too tired too punch stuff right now.",
    "You lost, go home kid...",
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


def get_random_victory_quote():
    return random.choice(VICTORY_QUOTES)


def get_random_defeat_message():
    return random.choice(DEFEAT_MESSAGES)


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
