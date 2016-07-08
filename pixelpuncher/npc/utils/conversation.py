import random
from annoying.functions import get_object_or_None

from pixelpuncher.game.utils.message import add_game_message
from pixelpuncher.game.utils.messages import pixels_dropped_message, xp_gained_message, item_dropped, item_given
from pixelpuncher.item.utils import add_item_type_to_player
from pixelpuncher.npc.models import ResponseTrigger, Triggers

MERCHANT_GREETINGS = [
    "Welcome to {}!",
    "Welcome!",
    "Can I help you?",
    "Welcome, can I help you?",
    "Welcome, what can I do to serve you?",
    "Hello, welcome to {}!",
    "Buy somethin' will ya!"
]

NPC_GREETINGS = [
    "Yes?",
    "What's up?",
    "Hey.",
    "Hello.",
    "How ya doing?",
    "What's happening?",
    "What's going on?",
    "How are things?",
]

NPC_GREETINGS_FORMAL = [
    "State your business.",
    "May I help you?",
    "Good morning.",
    "Good evening.",
]

def get_merchant_greeting(location):
    greeting = str(random.choice(MERCHANT_GREETINGS)).format(location.name)
    return '{} says "{}"'.format(location.npc.name, greeting)

#
# def get_merchant_greeting(location):
#     greeting = random.choice(GREETINGS)
#     return str(greeting).format(location.name)
#


def get_npc_greeting(npc):
    greeting = str(random.choice(NPC_GREETINGS))
    return '{} says "{}"'.format(npc.name, greeting)


def parse_trigger_text(text):
    trigger_type = ""
    output_text = ""

    if text.lower().startswith("ask about"):
        trigger_type = Triggers.ASK
        output_text = text[9:]
    elif text.lower().startswith("ask"):
        trigger_type = Triggers.ASK
        output_text = text[3:]
    elif text.lower().startswith("tell"):
        trigger_type = Triggers.TELL
        output_text = text[4:]
    elif text.lower().startswith("help"):
        trigger_type = Triggers.HELP

    return trigger_type, output_text.strip()


def get_response(npc, trigger_text, trigger_type):
    trigger = get_object_or_None(
        ResponseTrigger, npcs__in=[npc], trigger_text=trigger_text, trigger_type=trigger_type.upper())

    if trigger:
        return trigger.response
    else:
        return None


def response_reward(response, player, npc):
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
        add_game_message(player, item_given(npc, item))

    player.save()

