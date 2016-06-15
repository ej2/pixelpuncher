import random
from annoying.functions import get_object_or_None

from pixelpuncher.game.utils.game_settings import RARE_ENCOUNTER_FREQUENCY, ULTRA_RARE_ENCOUNTER_FREQUENCY
from pixelpuncher.game.utils.message import add_game_message
from pixelpuncher.game.utils.messages import xp_gained_message, pixels_dropped_message, item_dropped
from pixelpuncher.item.utils import add_item_type_to_player
from pixelpuncher.location.models import PlayerAdventure
from pixelpuncher.player.models import ADVENTURING


def get_adventure(player, location):
    player_adventure = get_current_adventure(player)

    if player_adventure is None:
        adventure = get_random_adventure(location)
        player_adventure = start_adventure(adventure=adventure, player=player)

        player.status = ADVENTURING
        player.punches -= 1
        player.save()

    return player_adventure


def get_current_adventure(player):
    return get_object_or_None(PlayerAdventure, active=True, player=player)


def get_random_adventure(location):
    frequency = random.randint(1, 100)

    if frequency < ULTRA_RARE_ENCOUNTER_FREQUENCY:
        adventures = location.adventures.filter(active=True, frequency="ULTRA")
    elif frequency < RARE_ENCOUNTER_FREQUENCY:
        adventures = location.adventures.filter(active=True, frequency="RARE")
    else:
        adventures = location.adventures.filter(active=True, frequency="COMMON")

    if adventures.count() == 0:
        adventures = location.adventures.filter(active=True)

    adventure = random.choice(adventures)
    return adventure


def start_adventure(player, adventure):
    player_adventure = PlayerAdventure(adventure=adventure, player=player)
    player_adventure.save()

    return player_adventure


def get_choice_results(choice, player):
    success = random.randint(1, 100)

    if success < choice.success_percentage:
        # SUCCESS!
        add_game_message(player, choice.success_text)
        choice_reward(choice, player)
    else:
        # FAILURE!
        add_game_message(player, choice.failure_text)


def choice_reward(choice, player):

    if choice.health_change != 0:
        add_game_message(player, player.adjust_health(choice.health_change))

    if choice.energy_change != 0:
        add_game_message(player, player.adjust_energy(choice.energy_change))

    if choice.pixels_change != 0:
        player.pixels += choice.pixels_change
        add_game_message(player, pixels_dropped_message(choice.pixels_change))

    if choice.xp_change > 0:
        player.xp += choice.xp_change
        add_game_message(player, xp_gained_message(choice.pixels_change))

    for item_type in choice.reward_items.all():
        item = add_item_type_to_player(item_type, player)
        add_game_message(player, item_dropped(item))

    player.save()

