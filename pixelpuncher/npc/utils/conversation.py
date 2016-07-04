import random
from annoying.functions import get_object_or_None

from pixelpuncher.game.utils.message import add_game_message
from pixelpuncher.game.utils.messages import pixels_dropped_message, xp_gained_message, item_dropped
from pixelpuncher.item.utils import add_item_type_to_player
from pixelpuncher.npc.models import ResponseTrigger

GREETINGS = [
    "Welcome to {}!",
    "Welcome!",
    "Can I help you?",
    "Welcome, can I help you?",
    "Welcome, what can I do to serve you?",
    "Hello, welcome to {}!",
    "Buy somethin' will ya!"
]


def get_merchant_greeting(location):
    greeting = str(random.choice(GREETINGS)).format(location.name)
    return '{} says "{}"'.format(location.npc.name, greeting)

#
# def get_merchant_greeting(location):
#     greeting = random.choice(GREETINGS)
#     return str(greeting).format(location.name)
#


def parse_trigger_text(text):
    trigger_type = ""

    if text.lower().startswith("ask"):
        trigger_type = 'ask'
    elif text.lower().startswith("tell"):
        trigger_type = 'tell'

    output_text = text.replace(trigger_type, '').strip()
    return trigger_type, output_text


def get_response(npc, trigger_text, trigger_type):
    trigger = get_object_or_None(
        ResponseTrigger, npcs__in=[npc], trigger_text=trigger_text, trigger_type=trigger_type.upper())

    if trigger:
        return trigger.response
    else:
        return None


def response_reward(response, player):
    if response.health_change != 0:
        add_game_message(player, player.adjust_health(response.health_change))

    if response.energy_change != 0:
        add_game_message(player, player.adjust_energy(response.energy_change))

    if response.pixels_change != 0:
        player.pixels += response.pixels_change
        add_game_message(player, pixels_dropped_message(response.pixels_change))

    if response.xp_change > 0:
        player.xp += response.xp_change
        add_game_message(player, xp_gained_message(response.pixels_change))

    for item_type in response.reward_items.all():
        item = add_item_type_to_player(item_type, player)
        add_game_message(player, item_dropped(item))

    player.save()

