import random

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, get_object_or_404
from django.template import RequestContext
from django.template.response import TemplateResponse

from pixelpuncher.game.forms import CheatCodeForm
from pixelpuncher.game.models import CheatCode
from pixelpuncher.game.utils import game_settings
from pixelpuncher.game.utils.adventure import get_choice_results, get_adventure, get_current_adventure, start_adventure
from pixelpuncher.game.utils.cheatcodes import add_cheatcode, do_cheat
from pixelpuncher.game.utils.combat import perform_skip, perform_skill_in_combat, perform_taunt, perform_use_item
from pixelpuncher.game.utils.encounter import get_enemy
from pixelpuncher.game.utils.game import can_punch, daily_reset, reset_check
from pixelpuncher.game.utils.leveling import xp_required_for_level, level_up
from pixelpuncher.game.utils.message import add_game_message
from pixelpuncher.game.utils.messages import system_boot
from pixelpuncher.item.utils import get_combat_items
from pixelpuncher.location.models import Location, AdventureChoice
from pixelpuncher.player.decorators import player_required
from pixelpuncher.player.models import PlayerSkill, VICTORY, COMBAT, PASSIVE, ADVENTURING


@login_required
@player_required
def game_start(request, player):
    context = {
        "user": player.user,
        "player": player,
    }

    return TemplateResponse(
        request, "game/start.html", RequestContext(request, context))


@login_required
@player_required
def map(request, player):
    context = {
        "user": player.user,
        "player": player,
        "locations": player.locations.all(),
    }

    return TemplateResponse(
        request, "game/map.html", RequestContext(request, context))


@login_required
@player_required
def play(request, player):
    location_id = request.session.get('location_id', 0)
    location = get_object_or_404(Location, pk=location_id)
    can_punch_flag = can_punch(player)

    enemy = None
    player_adventure = None

    if reset_check(player):
        daily_reset(player)

    if can_punch_flag:
        if player.status == VICTORY:
            player.status = PASSIVE
            player.save()

        elif player.status == PASSIVE:
            if can_punch_flag:
                if random.randint(1, 100) < location.adventure_rate:
                    player_adventure = get_adventure(player, location)
                    player.status = ADVENTURING
                else:
                    enemy = get_enemy(player, location)
                    player.status = COMBAT

                player.save()

        elif player.status == COMBAT:
            enemy = get_enemy(player, location)

        elif player.status == ADVENTURING:
            player_adventure = get_adventure(player, location)

    context = {
        "user": player.user,
        "player": player,
        "combat_items": get_combat_items(player),
        "enemy": enemy,
        "player_adventure": player_adventure,
        "can_punch": can_punch_flag,
        "boot_up": system_boot(),
        "location": location
    }

    return TemplateResponse(
        request, "game/play.html", RequestContext(request, context))



@login_required
@player_required
def adventure_choice(request, player, choice_id):
    choice = get_object_or_404(AdventureChoice, pk=choice_id)

    player_adventure = get_current_adventure(player)
    player_adventure.choice_made = choice
    player_adventure.active = False
    player_adventure.save()

    get_choice_results(choice, player)

    if choice.follow_up_adventure:
        start_adventure(choice.follow_up_adventure)
    else:
        player.status = VICTORY
        player.save()

    return redirect(reverse("game:play"))


@login_required
@player_required
def use(request, player, item_id):
    perform_use_item(player, item_id)

    return redirect(reverse("game:play"))


@login_required
@player_required
def skill(request, player, player_skill_id):
    player_skill = get_object_or_404(PlayerSkill, id=player_skill_id)
    perform_skill_in_combat(player, player_skill)

    return redirect(reverse("game:play"))


@login_required
@player_required
def taunt(request, player):
    perform_taunt(player)
    return redirect(reverse("game:play"))


@player_required
def skip(request, player):
    perform_skip(player)
    return redirect(reverse("game:play"))


@login_required
@player_required
def reset(request, player):
    player.punches = game_settings.DAILY_PUNCHES
    player.current_health = player.total_health
    player.current_energy = player.total_energy
    player.save()

    return redirect(reverse("game:play"))


@player_required
def perform_daily_reset(request, player):
    daily_reset(player)

    return redirect(reverse("game:play"))


@login_required
@player_required
def perform_level_up(request, player):
    level_up(player)

    return redirect(reverse("game:play"))


@login_required
@player_required
def level_requirements(request, player):
    levels = []
    previous = 0

    for x in range(1, 21):
        xp = int(xp_required_for_level(x))
        levels.append({
            "level": x,
            "xp": xp,
            "diff": xp - previous
        })

        previous = xp

    context = {
        "levels": levels,
        "player": player
    }

    return TemplateResponse(
        request, "game/levels.html", RequestContext(request, context))


@login_required
@player_required
def cheat_code(request, player):
    if request.method == "POST":
        form = CheatCodeForm(request.POST)
        code = request.POST["code"]

        cheat_added = add_cheatcode(player, code)
        if cheat_added:
            add_game_message(player, "Cheat code {} unlocked!".format(code))
    else:
        form = CheatCodeForm()

    context = {
        "form": form,
        "player": player
    }

    return TemplateResponse(
        request, "game/cheatcode.html", RequestContext(request, context))


@login_required
@player_required
def perform_cheat(request, player, cheatcode_id):
    cheatcode = get_object_or_404(CheatCode, players__id__exact=player.id, id=cheatcode_id)
    result = do_cheat(player, cheatcode)

    add_game_message(player, result)
    return redirect(reverse("game:map"))
