import random

from annoying.functions import get_object_or_None
from datetime import datetime

from pixelpuncher.game.utils.message import add_game_message
from pixelpuncher.game.utils.messages import pixels_dropped_message, xp_gained_message, item_given, \
    location_unlocked_message
from pixelpuncher.item.utils import add_item_type_to_player
from pixelpuncher.location.utils import unlock_location
from pixelpuncher.npc.models import ResponseTrigger, Triggers, ResponseHandlers, ResponseLog
from pixelpuncher.npc.utils.relationships import get_relationship, adjust_relationship_score
from pixelpuncher.player.utils.collections import check_collections

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
    return get_saying(location.npc.name, NPC_GREETINGS)
    greeting = str(random.choice(MERCHANT_GREETINGS)).format(location.name)
    return '{} says "{}"'.format(location.npc.name, greeting)

#
# def get_merchant_greeting(location):
#     greeting = random.choice(GREETINGS)
#     return str(greeting).format(location.name)
#


def get_npc_greeting(npc):
    return get_saying(npc.name, NPC_GREETINGS)


def get_formal_npc_greeting(npc):
    return get_saying(npc.name, NPC_GREETINGS_FORMAL)


def get_saying(name, saying_list):
    saying = str(random.choice(saying_list))
    return '{} says "{}"'.format(name, saying)


def parse_trigger_text(text):
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
        output_text = text[4:]
    else:
        trigger_type = Triggers.ACKNOWLEDGE
        output_text = text

    return trigger_type, output_text.strip()


def get_response(player, npc, trigger_text, trigger_type):
    response = None
    trigger = get_object_or_None(
        ResponseTrigger, npcs__in=[npc], trigger_text=trigger_text, trigger_type=trigger_type.upper())

    if trigger:
        if trigger.responses.count() == 1:
            return trigger.responses.all()[0]
        else:
            if trigger.response_handler == ResponseHandlers.Random:
                response = random.choice(trigger.responses.all())
                return response

            elif trigger.response_handler == ResponseHandlers.Ordered:
                last_response = get_last_response(player, trigger)

                if last_response:
                    next_priority = last_response.priority + 1
                    next_response = trigger.responses.filter(priority=next_priority)
                    if next_response.count() > 0:
                        response = next_response[0]
                else:
                    response = trigger.responses.filter(priority=1)[0]

                if response:
                    log_response(player, response, trigger)
                    return response
                else:
                    return last_response
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

        check_collections(player, item_type)

    player.save()

    if response.location_unlock:
        unlock_location(player, response.location_unlock)
        add_game_message(player, location_unlocked_message(response.location_unlock.name))

    if response.relationship_points != 0:
        relationship = get_relationship(player, npc)
        adjust_relationship_score(relationship, response.relationship_points)


def log_response(player, response, trigger):
    log = ResponseLog(player=player, response=response, response_trigger=trigger, response_date=datetime.now())
    log.save()
    return log


def get_last_response(player, trigger):
    logs = ResponseLog.objects.filter(player=player, response_trigger=trigger).order_by("-response__priority")
    if logs.count() > 0:
        return logs[0].response
    else:
        return None
