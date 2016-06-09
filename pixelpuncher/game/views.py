from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, get_object_or_404
from django.template import RequestContext
from django.template.response import TemplateResponse

from pixelpuncher.game.utils import game_settings
from pixelpuncher.game.utils.combat import perform_skip, perform_skill, perform_taunt, perform_use_item
from pixelpuncher.game.utils.encounter import get_enemy
from pixelpuncher.game.utils.game import can_punch, daily_reset, reset_check
from pixelpuncher.game.utils.leveling import xp_required_for_level, level_up
from pixelpuncher.game.utils.message import get_game_messages
from pixelpuncher.game.utils.messages import begin_combat_sequence, system_boot
from pixelpuncher.item.models import Item
from pixelpuncher.item.utils import get_combat_items, use_item
from pixelpuncher.player.decorators import player_required
from pixelpuncher.player.models import PlayerSkill, VICTORY, COMBAT, PASSIVE


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
    combat_output = "Something"
    can_punch_flag = can_punch(player)

    enemy = None

    if reset_check(player):
        daily_reset(player)

    if can_punch_flag:
        if player.status == VICTORY:
            player.status = PASSIVE
            player.save()

        elif player.status == PASSIVE:
            if can_punch_flag:
                enemy = get_enemy(player)
                player.status = COMBAT
                player.save()
                combat_output = begin_combat_sequence(enemy)

        elif player.status == COMBAT:
            enemy = get_enemy(player)
            combat_output = begin_combat_sequence(enemy)

    context = {
        "user": player.user,
        "player": player,
        "combat_items": get_combat_items(player),
        "enemy": enemy,
        "can_punch": can_punch_flag,
        "combat_output": combat_output,
        "boot_up": system_boot()
    }

    return TemplateResponse(
        request, "game/play.html", RequestContext(request, context))


@login_required
@player_required
def use(request, player, item_id):
    perform_use_item(player, item_id)

    return redirect(reverse("game:play"))


@login_required
@player_required
def skill(request, player, player_skill_id):
    player_skill = get_object_or_404(PlayerSkill, id=player_skill_id)
    perform_skill(player, player_skill)

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

